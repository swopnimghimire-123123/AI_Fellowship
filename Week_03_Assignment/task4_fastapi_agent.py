"""
WEEK 3 - TASK 4: MINI SQL AGENT (AGENTIC SYSTEM)

A FastAPI-based agentic Text-to-SQL system with:
- Query understanding and decomposition
- SQL generation
- Execution and error handling
- Automatic retry and self-correction (up to 3 retries)
- Natural language response generation
- Comprehensive logging
"""

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
import logging
import json
import time
import psycopg2
from datetime import datetime
from enum import Enum

# ============================================================================
# CONFIGURATION
# ============================================================================

DATABASE_CONFIG = {
    "host": "localhost",
    "database": "sample_db",
    "user": "postgres",
    "password": "password",
    "port": 5432
}

LOG_DIR = "./logs"
LOG_FILE = f"{LOG_DIR}/agent_execution.log"

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class AgentRequest(BaseModel):
    """Request model for agent endpoint"""
    question: str = Field(..., description="Natural language question about the database")
    
    class Config:
        schema_extra = {
            "example": {
                "question": "How many customers are from USA?"
            }
        }


class DecompositionStep(BaseModel):
    """Decomposition output from agent"""
    intent: str
    tables: List[str]
    columns: List[str]
    filters: List[Dict[str, str]] = []
    joins: List[Dict[str, str]] = []
    aggregations: List[str] = []
    group_by: List[str] = []


class ExecutionLog(BaseModel):
    """Log entry for execution"""
    attempt: int
    sql: str
    success: bool
    error: Optional[str] = None
    latency_ms: float
    rows_returned: int = 0
    timestamp: str


class AgentResponse(BaseModel):
    """Response model for agent endpoint"""
    question: str
    sql: str
    result: Optional[List[Dict[str, Any]]]
    summary: str
    decomposition: DecompositionStep
    execution_logs: List[ExecutionLog]
    status: str  # "success", "success_after_retry", "failed"
    total_attempts: int
    total_latency_ms: float
    rows_affected: int
    error_message: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "question": "How many customers are from USA?",
                "sql": "SELECT COUNT(*) FROM customers WHERE country = 'USA';",
                "result": [{"COUNT": 36}],
                "summary": "There are 36 customers from USA.",
                "status": "success",
                "total_attempts": 1,
                "total_latency_ms": 145.3,
                "rows_affected": 1
            }
        }


# ============================================================================
# QUERY DECOMPOSER
# ============================================================================

class EnhancedQueryDecomposer:
    """
    Enhanced decomposer with better pattern recognition
    """
    
    TABLE_KEYWORDS = {
        "product": ["products", "productlines"],
        "customer": ["customers"],
        "order": ["orders", "orderdetails"],
        "employee": ["employees"],
        "office": ["offices"],
        "payment": ["payments"]
    }
    
    def decompose(self, question: str) -> DecompositionStep:
        """Decompose question into structured components"""
        logger.info(f"Agent decomposing: {question}")
        
        q_lower = question.lower()
        
        # Detect intent
        intent = self._detect_intent(q_lower)
        
        # Detect tables
        tables = self._detect_tables(q_lower)
        
        # Detect columns
        columns = self._detect_columns(q_lower, tables)
        
        # Detect filters
        filters = self._detect_filters(q_lower)
        
        # Detect joins
        joins = self._detect_joins(tables, q_lower)
        
        # Detect aggregations
        aggregations = self._detect_aggregations(q_lower)
        
        # Detect GROUP BY
        group_by = self._detect_group_by(q_lower)
        
        return DecompositionStep(
            intent=intent,
            tables=tables,
            columns=columns,
            filters=filters,
            joins=joins,
            aggregations=aggregations,
            group_by=group_by
        )
    
    def _detect_intent(self, q: str) -> str:
        """Detect query intent"""
        if "count" in q:
            return "count"
        elif "sum" in q or "total" in q or "revenue" in q:
            return "sum"
        elif "average" in q or "avg" in q:
            return "average"
        elif "max" in q or "maximum" in q or "highest" in q:
            return "max"
        elif "min" in q or "minimum" in q or "lowest" in q:
            return "min"
        elif "per" in q or "by" in q or "for each" in q:
            return "group_by"
        elif "with" in q and any(word in q for word in ["and", "their", "from"]):
            return "join"
        else:
            return "select"
    
    def _detect_tables(self, q: str) -> List[str]:
        """Detect involved tables"""
        tables = set()
        
        if "product" in q:
            tables.add("products")
        if "customer" in q:
            tables.add("customers")
        if "order" in q:
            tables.add("orders")
            if "detail" in q:
                tables.add("orderdetails")
        if "employee" in q:
            tables.add("employees")
        if "office" in q:
            tables.add("offices")
        if "payment" in q:
            tables.add("payments")
        
        if not tables:
            tables.add("products")
        
        return sorted(list(tables))
    
    def _detect_columns(self, q: str, tables: List[str]) -> List[str]:
        """Detect needed columns"""
        columns = []
        
        # Add primary keys
        for table in tables:
            if "product" in table:
                columns.append("productName")
            elif "customer" in table:
                columns.append("customerName")
            elif "order" in table:
                columns.append("orderNumber")
            elif "employee" in table:
                columns.append("firstName")
                columns.append("lastName")
            elif "payment" in table:
                columns.append("amount")
        
        # Check for specific columns mentioned
        if "price" in q:
            columns.extend(["buyPrice", "MSRP"])
        if "city" in q:
            columns.append("city")
        if "country" in q:
            columns.append("country")
        if "status" in q:
            columns.append("status")
        if "date" in q:
            columns.append("orderDate")
        
        if not columns or "count" in q:
            columns = ["*"] if "list" in q or "all" in q else columns
        
        return list(set(columns)) if columns else ["*"]
    
    def _detect_filters(self, q: str) -> List[Dict[str, str]]:
        """Detect WHERE conditions"""
        filters = []
        
        if "usa" in q:
            filters.append({"column": "country", "operator": "=", "value": "USA"})
        elif "germany" in q:
            filters.append({"column": "country", "operator": "=", "value": "Germany"})
        elif "france" in q:
            filters.append({"column": "country", "operator": "=", "value": "France"})
        
        if "shipped" in q:
            filters.append({"column": "status", "operator": "=", "value": "Shipped"})
        
        return filters
    
    def _detect_joins(self, tables: List[str], q: str) -> List[Dict[str, str]]:
        """Detect JOIN operations"""
        joins = []
        
        if len(tables) <= 1:
            return joins
        
        if "orders" in tables and "customers" in tables:
            joins.append({
                "table1": "orders",
                "table2": "customers",
                "type": "INNER",
                "condition": "o.customerNumber = c.customerNumber"
            })
        
        if "employees" in tables and "offices" in tables:
            joins.append({
                "table1": "employees",
                "table2": "offices",
                "type": "INNER",
                "condition": "e.officeCode = o.officeCode"
            })
        
        if "payments" in tables and "customers" in tables:
            joins.append({
                "table1": "payments",
                "table2": "customers",
                "type": "INNER",
                "condition": "p.customerNumber = c.customerNumber"
            })
        
        if "manager" in q and "employees" in tables:
            joins.append({
                "table1": "employees",
                "table2": "employees",
                "type": "LEFT",
                "condition": "e.reportsTo = m.employeeNumber"
            })
        
        return joins
    
    def _detect_aggregations(self, q: str) -> List[str]:
        """Detect aggregation functions"""
        aggs = []
        
        if "count" in q:
            aggs.append("COUNT")
        if "sum" in q or "total" in q:
            aggs.append("SUM")
        if "average" in q or "avg" in q:
            aggs.append("AVG")
        if "max" in q or "highest" in q:
            aggs.append("MAX")
        if "min" in q or "lowest" in q:
            aggs.append("MIN")
        
        return aggs
    
    def _detect_group_by(self, q: str) -> List[str]:
        """Detect GROUP BY columns"""
        if "per" in q or "for each" in q or "by" in q:
            if "country" in q:
                return ["country"]
            elif "city" in q:
                return ["city"]
            elif "status" in q:
                return ["status"]
            elif "line" in q:
                return ["productLine"]
            elif "vendor" in q:
                return ["productVendor"]
            elif "customer" in q:
                return ["customerName"]
        
        return []


# ============================================================================
# SQL GENERATOR
# ============================================================================

class AgentSQLGenerator:
    """Generate SQL from decomposition"""
    
    def generate(self, decomp: DecompositionStep, question: str) -> str:
        """Generate SQL query"""
        logger.info(f"Generating SQL for decomposition: {decomp}")
        
        # Build SELECT
        if decomp.aggregations:
            select_parts = [f"{agg}(*)" if agg == "COUNT" else f"{agg}(amount)" 
                          for agg in decomp.aggregations]
            select_clause = f"SELECT {', '.join(select_parts)}"
        else:
            cols = ", ".join(decomp.columns) if decomp.columns and decomp.columns != ["*"] else "*"
            select_clause = f"SELECT {cols}"
        
        # Build FROM
        main_table = decomp.tables[0] if decomp.tables else "products"
        alias = main_table[0]
        from_clause = f"FROM {main_table} {alias}"
        
        # Build JOINs
        joins_sql = ""
        for join in decomp.joins:
            join_type = join.get("type", "INNER")
            t1, t2 = join["table1"], join["table2"]
            cond = join["condition"]
            joins_sql += f"\n{join_type} JOIN {t2} ON {cond}"
        
        # Build WHERE
        where_sql = ""
        if decomp.filters:
            conditions = [f"{f['column']} {f['operator']} '{f['value']}'" 
                         for f in decomp.filters]
            where_sql = f"\nWHERE {' AND '.join(conditions)}"
        
        # Build GROUP BY
        group_sql = ""
        if decomp.group_by:
            group_sql = f"\nGROUP BY {', '.join(decomp.group_by)}"
        
        sql = select_clause + "\n" + from_clause + joins_sql + where_sql + group_sql + ";"
        
        logger.info(f"Generated SQL:\n{sql}")
        return sql


# ============================================================================
# QUERY EXECUTOR WITH RETRY
# ============================================================================

class AgentQueryExecutor:
    """Execute queries with automatic retry and error handling"""
    
    MAX_RETRIES = 3
    BLOCKED_KEYWORDS = ["DROP", "DELETE", "INSERT", "UPDATE", "ALTER"]
    
    def __init__(self, db_config: Dict = None):
        self.db_config = db_config or DATABASE_CONFIG
    
    def execute(self, sql: str, question: str, decomp: DecompositionStep) -> tuple:
        """
        Execute query with retry logic.
        Returns: (success, result, logs, error_msg)
        """
        logger.info(f"Executing SQL with retry logic (max {self.MAX_RETRIES} attempts)")
        
        # Validate
        if not self._is_safe(sql):
            return False, None, [], "Query contains blocked keywords"
        
        logs = []
        last_error = None
        result = None
        
        for attempt in range(1, self.MAX_RETRIES + 1):
            start = time.time()
            
            try:
                logger.info(f"Attempt {attempt}: Executing query")
                
                conn = psycopg2.connect(**self.db_config)
                cursor = conn.cursor()
                
                cursor.execute(sql)
                conn.commit()
                
                # Fetch results
                if cursor.description:
                    columns = [desc[0] for desc in cursor.description]
                    rows = cursor.fetchall()
                    result = [dict(zip(columns, row)) for row in rows]
                else:
                    result = []
                
                latency = (time.time() - start) * 1000
                
                log_entry = ExecutionLog(
                    attempt=attempt,
                    sql=sql,
                    success=True,
                    latency_ms=latency,
                    rows_returned=len(result) if result else 0,
                    timestamp=datetime.now().isoformat()
                )
                logs.append(log_entry)
                
                cursor.close()
                conn.close()
                
                logger.info(f"Query succeeded on attempt {attempt}")
                return True, result, logs, None
            
            except Exception as e:
                latency = (time.time() - start) * 1000
                last_error = str(e)
                
                logger.error(f"Attempt {attempt} failed: {last_error}")
                
                log_entry = ExecutionLog(
                    attempt=attempt,
                    sql=sql,
                    success=False,
                    error=last_error,
                    latency_ms=latency,
                    timestamp=datetime.now().isoformat()
                )
                logs.append(log_entry)
                
                # Attempt fix
                if attempt < self.MAX_RETRIES:
                    fixed_sql = self._attempt_fix(sql, last_error)
                    if fixed_sql != sql:
                        logger.info(f"Query fixed, retrying...")
                        sql = fixed_sql
                    else:
                        logger.info(f"No fix possible, will retry original")
        
        logger.error(f"All {self.MAX_RETRIES} attempts failed")
        return False, result, logs, last_error
    
    def _is_safe(self, sql: str) -> bool:
        """Check if query is safe"""
        sql_upper = sql.strip().upper()
        
        for kw in self.BLOCKED_KEYWORDS:
            if kw in sql_upper:
                return False
        
        if not sql_upper.startswith("SELECT"):
            return False
        
        return True
    
    def _attempt_fix(self, sql: str, error: str) -> str:
        """Attempt to fix broken query"""
        
        if "column" in error.lower():
            # Try adding proper quoting
            sql = sql.replace('COUNT(*)', 'COUNT(DISTINCT customerNumber)')
        
        return sql


# ============================================================================
# NATURAL LANGUAGE GENERATOR
# ============================================================================

class NLGenerator:
    """Convert query results to natural language"""
    
    def generate_summary(self, question: str, result: List[Dict], sql: str) -> str:
        """Generate natural language summary from results"""
        
        if not result:
            return "No results found for your query."
        
        if len(result) == 1:
            row = result[0]
            first_key = list(row.keys())[0]
            value = row[first_key]
            
            if "count" in first_key.lower():
                return f"There are {value} records matching your query."
            elif "sum" in first_key.lower() or "total" in first_key.lower():
                return f"The total is {value}."
            elif "average" in first_key.lower() or "avg" in first_key.lower():
                return f"The average is {value}."
            elif "max" in first_key.lower():
                return f"The maximum value is {value}."
            elif "min" in first_key.lower():
                return f"The minimum value is {value}."
            else:
                return f"Result: {value}"
        else:
            return f"Found {len(result)} records matching your query."
    
    def summarize(self, question: str, result: List[Dict], decomp: DecompositionStep) -> str:
        """Create comprehensive summary"""
        
        if not result:
            return "No results found."
        
        # Check aggregation type
        if decomp.aggregations:
            agg = decomp.aggregations[0]
            if agg == "COUNT":
                count = list(result[0].values())[0] if result[0] else 0
                return f"There are {count} results."
            elif agg == "SUM":
                total = list(result[0].values())[0] if result[0] else 0
                return f"The total is {total}."
            elif agg == "AVG":
                avg = list(result[0].values())[0] if result[0] else 0
                return f"The average is {avg:.2f}."
        
        # Check for GROUP BY
        if decomp.group_by:
            return f"Found {len(result)} groups in the results."
        
        # Default
        return f"Query returned {len(result)} records."


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

app = FastAPI(
    title="SQL Agent API",
    description="AI-powered Text-to-SQL agent with agentic capabilities",
    version="1.0.0"
)

# Initialize components
decomposer = EnhancedQueryDecomposer()
generator = AgentSQLGenerator()
executor = AgentQueryExecutor()
nl_gen = NLGenerator()


@app.post("/agent/sql", response_model=AgentResponse)
async def agent_sql(request: AgentRequest):
    """
    Main agent endpoint.
    
    Takes a natural language question and returns:
    - Decomposition
    - Generated SQL
    - Execution results
    - Natural language summary
    """
    
    question = request.question
    logger.info(f"=== NEW AGENT REQUEST ===")
    logger.info(f"Question: {question}")
    
    try:
        # Step 1: Decompose question
        logger.info("Step 1: Decomposing question...")
        decomposition = decomposer.decompose(question)
        logger.info(f"Decomposition: {decomposition}")
        
        # Step 2: Generate SQL
        logger.info("Step 2: Generating SQL...")
        sql = generator.generate(decomposition, question)
        logger.info(f"Generated SQL: {sql}")
        
        # Step 3: Execute query with retry
        logger.info("Step 3: Executing query...")
        success, result, execution_logs, error_msg = executor.execute(sql, question, decomposition)
        
        # Step 4: Generate summary
        if success:
            logger.info("Step 4: Generating natural language summary...")
            summary = nl_gen.summarize(question, result, decomposition)
            
            status = "success" if len(execution_logs) == 1 else "success_after_retry"
            total_latency = sum(log.latency_ms for log in execution_logs)
            rows_affected = sum(log.rows_returned for log in execution_logs)
        else:
            summary = f"Query failed after {len(execution_logs)} attempts: {error_msg}"
            status = "failed"
            total_latency = sum(log.latency_ms for log in execution_logs)
            rows_affected = 0
        
        # Step 5: Return response
        response = AgentResponse(
            question=question,
            sql=sql,
            result=result,
            summary=summary,
            decomposition=decomposition,
            execution_logs=execution_logs,
            status=status,
            total_attempts=len(execution_logs),
            total_latency_ms=total_latency,
            rows_affected=rows_affected,
            error_message=error_msg
        )
        
        logger.info(f"Response: {response.status}")
        return response
    
    except Exception as e:
        logger.error(f"Agent error: {str(e)}", exc_info=True)
        
        raise HTTPException(
            status_code=500,
            detail=f"Agent processing failed: {str(e)}"
        )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.get("/")
async def root():
    """Root endpoint with API documentation"""
    return {
        "name": "SQL Agent API",
        "version": "1.0.0",
        "description": "AI-powered Text-to-SQL agent",
        "endpoints": {
            "POST /agent/sql": "Process natural language question",
            "GET /health": "Health check"
        }
    }


# ============================================================================
# EXAMPLE USAGE & TESTING
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    print("""
    ╔═════════════════════════════════════════════════════════════╗
    ║        WEEK 3 TASK 4: SQL AGENT API                        ║
    ║    Text-to-SQL Agentic System with Auto-Retry              ║
    ╚═════════════════════════════════════════════════════════════╝
    
    Starting FastAPI server...
    
    API Endpoint: POST http://localhost:8000/agent/sql
    
    Example Request:
    {
        "question": "How many customers are from USA?"
    }
    
    Example Response:
    {
        "question": "How many customers are from USA?",
        "sql": "SELECT COUNT(*) FROM customers WHERE country = 'USA';",
        "result": [{"COUNT": 36}],
        "summary": "There are 36 customers from USA.",
        "status": "success",
        "total_attempts": 1,
        "total_latency_ms": 145.3,
        "rows_affected": 1,
        "decomposition": { ... },
        "execution_logs": [ ... ]
    }
    
    Documentation: http://localhost:8000/docs
    """)
    
    uvicorn.run(app, host="0.0.0.0", port=8000)

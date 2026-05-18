"""
WEEK 3 - TASK 3: TEXT-TO-SQL PIPELINE AND QUERY EXECUTION SYSTEM

A complete Text-to-SQL pipeline that:
1. Takes natural language questions
2. Decomposes them into structured components
3. Generates SQL queries
4. Executes them safely against PostgreSQL
5. Handles errors and retries
6. Returns structured results
"""

import json
import logging
import time
import psycopg2
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
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
QUERY_LOG_FILE = f"{LOG_DIR}/query_execution.log"
DECOMPOSITION_LOG_FILE = f"{LOG_DIR}/decomposition.log"

# ============================================================================
# LOGGING SETUP
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# DATA MODELS
# ============================================================================

class IntentType(Enum):
    """Query intent classification"""
    SELECT_ALL = "select_all"
    PROJECTION = "projection"
    DISTINCT = "distinct"
    JOIN = "join"
    AGGREGATION = "aggregation"
    AGGREGATION_WITH_JOIN = "aggregation_with_join"
    GROUP_BY = "group_by"
    FILTER = "filter"
    UNKNOWN = "unknown"


@dataclass
class QueryDecomposition:
    """Structured decomposition of a natural language question"""
    question: str
    intent: IntentType
    primary_tables: List[str]
    columns: List[str]
    filters: List[Dict[str, str]]  # [{column, operator, value}]
    joins: List[Dict[str, str]]  # [{table1, table2, condition}]
    aggregations: List[str]  # [COUNT, SUM, AVG, etc.]
    group_by: List[str]
    order_by: List[Tuple[str, str]]  # [(column, ASC/DESC)]
    distinct: bool
    limit: Optional[int]
    
    def to_dict(self):
        return asdict(self)


@dataclass
class QueryExecution:
    """Result of query execution"""
    question: str
    sql: str
    decomposition: QueryDecomposition
    success: bool
    result: Optional[List[Dict]] = None
    error: Optional[str] = None
    execution_time_ms: float = 0
    rows_affected: int = 0
    retry_count: int = 0
    retry_details: List[str] = None
    
    def to_dict(self):
        return {
            "question": self.question,
            "sql": self.sql,
            "decomposition": self.decomposition.to_dict(),
            "success": self.success,
            "result": self.result,
            "error": self.error,
            "execution_time_ms": self.execution_time_ms,
            "rows_affected": self.rows_affected,
            "retry_count": self.retry_count,
            "retry_details": self.retry_details or []
        }


# ============================================================================
# QUERY DECOMPOSER
# ============================================================================

class QueryDecomposer:
    """
    Breaks natural language questions into structured components.
    Uses keyword pattern matching and heuristics.
    """
    
    # Database schema knowledge
    TABLE_KEYWORDS = {
        "product": ["products", "productlines"],
        "customer": ["customers"],
        "order": ["orders", "orderdetails"],
        "employee": ["employees"],
        "office": ["offices"],
        "payment": ["payments"]
    }
    
    COLUMN_MAP = {
        "name": ["productName", "customerName", "firstName", "lastName"],
        "price": ["buyPrice", "MSRP", "priceEach"],
        "count": ["COUNT"],
        "quantity": ["quantityInStock", "quantityOrdered"],
        "date": ["orderDate", "paymentDate", "requiredDate", "shippedDate"],
        "status": ["status"],
        "vendor": ["productVendor"],
        "city": ["city"],
        "country": ["country"],
        "amount": ["amount"]
    }
    
    def decompose(self, question: str) -> QueryDecomposition:
        """
        Decompose a natural language question into structured components.
        
        Args:
            question: Natural language question
            
        Returns:
            QueryDecomposition object with all components
        """
        logger.info(f"Decomposing question: {question}")
        
        question_lower = question.lower()
        
        # Detect intent
        intent = self._detect_intent(question_lower)
        
        # Detect tables
        primary_tables = self._detect_tables(question_lower)
        
        # Detect columns
        columns = self._detect_columns(question_lower, primary_tables)
        
        # Detect filters
        filters = self._detect_filters(question_lower)
        
        # Detect joins
        joins = self._detect_joins(primary_tables, question_lower)
        
        # Detect aggregations
        aggregations = self._detect_aggregations(question_lower)
        
        # Detect GROUP BY
        group_by = self._detect_group_by(question_lower, columns)
        
        # Detect ORDER BY
        order_by = self._detect_order_by(question_lower)
        
        # Detect DISTINCT
        distinct = "distinct" in question_lower or "unique" in question_lower
        
        # Detect LIMIT
        limit = self._detect_limit(question_lower)
        
        decomposition = QueryDecomposition(
            question=question,
            intent=intent,
            primary_tables=primary_tables,
            columns=columns,
            filters=filters,
            joins=joins,
            aggregations=aggregations,
            group_by=group_by,
            order_by=order_by,
            distinct=distinct,
            limit=limit
        )
        
        logger.info(f"Decomposition: {decomposition}")
        return decomposition
    
    def _detect_intent(self, question: str) -> IntentType:
        """Detect the query intent"""
        if "count" in question:
            return IntentType.AGGREGATION
        elif "sum" in question or "total" in question:
            return IntentType.AGGREGATION
        elif "average" in question or "avg" in question:
            return IntentType.AGGREGATION
        elif "max" in question or "maximum" in question:
            return IntentType.AGGREGATION
        elif "min" in question or "minimum" in question:
            return IntentType.AGGREGATION
        elif "list" in question and "with" in question:
            return IntentType.JOIN
        elif "get" in question and "with" in question:
            return IntentType.JOIN
        elif "per" in question or "for each" in question:
            return IntentType.GROUP_BY
        elif "distinct" in question or "unique" in question:
            return IntentType.DISTINCT
        elif any(word in question for word in ["all", "list", "show", "get"]):
            return IntentType.SELECT_ALL
        else:
            return IntentType.PROJECTION
    
    def _detect_tables(self, question: str) -> List[str]:
        """Detect which tables are involved"""
        tables = set()
        
        for keyword, table_list in self.TABLE_KEYWORDS.items():
            if keyword in question:
                tables.update(table_list)
        
        # Handle multi-table scenarios based on specific phrases
        if ("order" in question and "customer" in question) or "order with customer" in question:
            tables = {"orders", "customers"}
        elif "employee" in question and ("office" in question or "city" in question):
            tables = {"employees", "offices"}
        elif ("employee" in question and "manager" in question):
            tables = {"employees"}  # Self-join
        elif "payment" in question and "customer" in question:
            tables = {"payments", "customers"}
        elif "orderdetail" in question or "order detail" in question:
            tables = {"orderdetails", "products"}
        
        return list(tables) if tables else ["products"]
    
    def _detect_columns(self, question: str, tables: List[str]) -> List[str]:
        """Detect which columns are needed"""
        if "*" in question or "all" in question:
            return ["*"]
        
        columns = []
        
        # Add ID columns
        for table in tables:
            if "product" in table:
                columns.append("productCode")
            elif "customer" in table:
                columns.append("customerNumber")
            elif "order" in table and "detail" not in table:
                columns.append("orderNumber")
            elif "employee" in table:
                columns.append("employeeNumber")
        
        # Add name columns
        if "product" in str(tables):
            columns.append("productName")
        if "customer" in str(tables):
            columns.append("customerName")
        
        # Add specific keywords
        if "price" in question:
            columns.extend(["buyPrice", "MSRP"])
        if "name" in question:
            columns.extend(["firstName", "lastName"])
        if "city" in question:
            columns.append("city")
        if "country" in question:
            columns.append("country")
        if "date" in question:
            columns.extend(["orderDate", "paymentDate"])
        
        return list(set(columns)) if columns else ["*"]
    
    def _detect_filters(self, question: str) -> List[Dict]:
        """Detect WHERE clause filters"""
        filters = []
        
        # Pattern: "customers from USA"
        if "from" in question:
            if "usa" in question:
                filters.append({"column": "country", "operator": "=", "value": "USA"})
            elif "germany" in question:
                filters.append({"column": "country", "operator": "=", "value": "Germany"})
        
        return filters
    
    def _detect_joins(self, tables: List[str], question: str) -> List[Dict]:
        """Detect JOIN operations"""
        joins = []
        
        if len(tables) <= 1:
            return joins
        
        tables_list = list(tables)
        
        # Self-join for employees and managers
        if "employee" in str(tables) and "manager" in question:
            joins.append({
                "table1": "employees",
                "table2": "employees",
                "condition": "e.reportsTo = m.employeeNumber",
                "type": "LEFT"
            })
            return joins
        
        # Orders with Customers
        if "orders" in tables_list and "customers" in tables_list:
            joins.append({
                "table1": "orders",
                "table2": "customers",
                "condition": "o.customerNumber = c.customerNumber",
                "type": "INNER"
            })
        
        # Employees with Offices
        elif "employees" in tables_list and "offices" in tables_list:
            joins.append({
                "table1": "employees",
                "table2": "offices",
                "condition": "e.officeCode = o.officeCode",
                "type": "INNER"
            })
        
        # Payments with Customers
        elif "payments" in tables_list and "customers" in tables_list:
            joins.append({
                "table1": "payments",
                "table2": "customers",
                "condition": "p.customerNumber = c.customerNumber",
                "type": "INNER"
            })
        
        # OrderDetails with Products
        elif "orderdetails" in tables_list and "products" in tables_list:
            joins.append({
                "table1": "orderdetails",
                "table2": "products",
                "condition": "od.productCode = p.productCode",
                "type": "INNER"
            })
        
        # Products with ProductLines
        elif "products" in tables_list and "productlines" in tables_list:
            joins.append({
                "table1": "products",
                "table2": "productlines",
                "condition": 'p."productLine" = pl."productLine"',
                "type": "INNER"
            })
        
        return joins
    
    def _detect_aggregations(self, question: str) -> List[str]:
        """Detect aggregate functions"""
        aggregations = []
        
        if "count" in question:
            aggregations.append("COUNT")
        if "sum" in question or "total" in question:
            aggregations.append("SUM")
        if "average" in question or "avg" in question:
            aggregations.append("AVG")
        if "max" in question or "maximum" in question:
            aggregations.append("MAX")
        if "min" in question or "minimum" in question:
            aggregations.append("MIN")
        
        return aggregations
    
    def _detect_group_by(self, question: str, columns: List[str]) -> List[str]:
        """Detect GROUP BY columns"""
        if "per" in question or "for each" in question or "by" in question:
            # Extract column from question
            if "country" in question:
                return ["country"]
            elif "vendor" in question or "supplier" in question:
                return ["productVendor"]
            elif "city" in question:
                return ["city"]
            elif "status" in question:
                return ["status"]
            elif "line" in question:
                return ["productLine"]
            elif "customer" in question:
                return ["customerName"]
            elif "office" in question:
                return ["city"]
        
        return []
    
    def _detect_order_by(self, question: str) -> List[Tuple[str, str]]:
        """Detect ORDER BY columns"""
        order_by = []
        
        if "highest" in question or "most" in question or "largest" in question:
            order_by.append(("count", "DESC"))
        elif "lowest" in question or "least" in question or "smallest" in question:
            order_by.append(("count", "ASC"))
        
        return order_by
    
    def _detect_limit(self, question: str) -> Optional[int]:
        """Detect LIMIT clause"""
        # Check for numbers like "top 10"
        if "top" in question:
            parts = question.split()
            for i, part in enumerate(parts):
                if part == "top" and i + 1 < len(parts):
                    try:
                        return int(parts[i + 1])
                    except ValueError:
                        pass
        
        return None


# ============================================================================
# SQL GENERATOR
# ============================================================================

class SQLGenerator:
    """
    Generates SQL queries from structured decompositions.
    """
    
    def generate(self, decomposition: QueryDecomposition) -> str:
        """
        Generate SQL query from decomposition.
        
        Args:
            decomposition: QueryDecomposition object
            
        Returns:
            SQL query string
        """
        logger.info(f"Generating SQL for: {decomposition.question}")
        
        # Build SELECT clause
        select_clause = self._build_select_clause(decomposition)
        
        # Build FROM clause
        from_clause = self._build_from_clause(decomposition)
        
        # Build JOIN clause
        join_clause = self._build_join_clause(decomposition)
        
        # Build WHERE clause
        where_clause = self._build_where_clause(decomposition)
        
        # Build GROUP BY clause
        group_by_clause = self._build_group_by_clause(decomposition)
        
        # Build ORDER BY clause
        order_by_clause = self._build_order_by_clause(decomposition)
        
        # Combine all clauses
        sql = select_clause
        if from_clause:
            sql += "\n" + from_clause
        if join_clause:
            sql += "\n" + join_clause
        if where_clause:
            sql += "\n" + where_clause
        if group_by_clause:
            sql += "\n" + group_by_clause
        if order_by_clause:
            sql += "\n" + order_by_clause
        
        sql += ";"
        logger.info(f"Generated SQL: {sql}")
        return sql
    
    def _build_select_clause(self, decomp: QueryDecomposition) -> str:
        """Build SELECT clause"""
        if decomp.distinct:
            return f'SELECT DISTINCT {", ".join(decomp.columns)}'
        else:
            return f'SELECT {", ".join(decomp.columns)}'
    
    def _build_from_clause(self, decomp: QueryDecomposition) -> str:
        """Build FROM clause"""
        if not decomp.primary_tables:
            return "FROM products"
        
        main_table = decomp.primary_tables[0]
        
        # Add table aliases
        if main_table == "orders":
            return f'FROM {main_table} o'
        elif main_table == "customers":
            return f'FROM {main_table} c'
        elif main_table == "products":
            return f'FROM {main_table} p'
        elif main_table == "employees":
            return f'FROM {main_table} e'
        elif main_table == "payments":
            return f'FROM {main_table} p'
        elif main_table == "orderdetails":
            return f'FROM {main_table} od'
        else:
            return f'FROM {main_table}'
    
    def _build_join_clause(self, decomp: QueryDecomposition) -> str:
        """Build JOIN clauses"""
        if not decomp.joins:
            return ""
        
        join_sql = ""
        for join in decomp.joins:
            join_type = join.get("type", "INNER")
            condition = join.get("condition", "")
            
            if join_type == "LEFT":
                join_sql += f'LEFT JOIN {join["table2"]} m ON {condition}'
            else:
                join_sql += f'JOIN {join["table2"]} {join["table2"][0]} ON {condition}'
        
        return join_sql
    
    def _build_where_clause(self, decomp: QueryDecomposition) -> str:
        """Build WHERE clause"""
        if not decomp.filters:
            return ""
        
        conditions = []
        for filter_item in decomp.filters:
            column = filter_item.get("column", "")
            operator = filter_item.get("operator", "=")
            value = filter_item.get("value", "")
            
            conditions.append(f'{column} {operator} \'{value}\'')
        
        if conditions:
            return "WHERE " + " AND ".join(conditions)
        return ""
    
    def _build_group_by_clause(self, decomp: QueryDecomposition) -> str:
        """Build GROUP BY clause"""
        if not decomp.group_by:
            return ""
        
        return f'GROUP BY {", ".join(decomp.group_by)}'
    
    def _build_order_by_clause(self, decomp: QueryDecomposition) -> str:
        """Build ORDER BY clause"""
        if not decomp.order_by:
            return ""
        
        order_items = [f'{col} {direction}' for col, direction in decomp.order_by]
        return f'ORDER BY {", ".join(order_items)}'


# ============================================================================
# QUERY EXECUTOR
# ============================================================================

class QueryExecutor:
    """
    Executes SQL queries safely against PostgreSQL.
    """
    
    # Blocked keywords for safety
    BLOCKED_KEYWORDS = ["DROP", "DELETE", "INSERT", "UPDATE", "ALTER", "TRUNCATE"]
    
    def __init__(self, db_config: Dict = None):
        """Initialize executor with database config"""
        self.db_config = db_config or DATABASE_CONFIG
    
    def execute(self, sql: str, max_retries: int = 1) -> QueryExecution:
        """
        Execute SQL query with error handling and retry logic.
        
        Args:
            sql: SQL query to execute
            max_retries: Maximum number of retry attempts
            
        Returns:
            QueryExecution object with results
        """
        logger.info(f"Executing query: {sql}")
        
        # Validate query safety
        if not self._is_safe_query(sql):
            return QueryExecution(
                question="",
                sql=sql,
                decomposition=None,
                success=False,
                error="Query contains blocked keywords (write operations not allowed)"
            )
        
        start_time = time.time()
        retry_count = 0
        last_error = None
        retry_details = []
        
        while retry_count <= max_retries:
            try:
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
                
                execution_time = (time.time() - start_time) * 1000
                
                cursor.close()
                conn.close()
                
                logger.info(f"Query succeeded in {execution_time}ms")
                
                return QueryExecution(
                    question="",
                    sql=sql,
                    decomposition=None,
                    success=True,
                    result=result,
                    execution_time_ms=execution_time,
                    rows_affected=cursor.rowcount if cursor.rowcount else len(result),
                    retry_count=retry_count
                )
            
            except Exception as e:
                last_error = str(e)
                logger.error(f"Query execution failed: {last_error}")
                
                if retry_count < max_retries:
                    retry_count += 1
                    retry_details.append(f"Attempt {retry_count}: {last_error}")
                    
                    # Try to fix query
                    fixed_sql = self._attempt_fix(sql, last_error)
                    if fixed_sql != sql:
                        logger.info(f"Retrying with fixed query...")
                        sql = fixed_sql
                        retry_details.append(f"Attempt {retry_count}: Query fixed and retried")
                else:
                    break
        
        execution_time = (time.time() - start_time) * 1000
        
        return QueryExecution(
            question="",
            sql=sql,
            decomposition=None,
            success=False,
            error=last_error,
            execution_time_ms=execution_time,
            retry_count=retry_count,
            retry_details=retry_details
        )
    
    def _is_safe_query(self, sql: str) -> bool:
        """Check if query is safe (SELECT only)"""
        sql_upper = sql.strip().upper()
        
        # Check for blocked keywords
        for keyword in self.BLOCKED_KEYWORDS:
            if keyword in sql_upper:
                return False
        
        # Must be SELECT
        if not sql_upper.startswith("SELECT"):
            return False
        
        return True
    
    def _attempt_fix(self, sql: str, error: str) -> str:
        """Attempt to fix a broken query based on error message"""
        
        # Common fixes
        if "column" in error.lower() and "does not exist" in error.lower():
            # Try adding quotes around identifiers
            sql = sql.replace(' ', ' "').replace('"FROM', ' FROM')
        
        elif "syntax error" in error.lower():
            # Try to identify and fix common syntax issues
            if "GROUP BY" in sql and "COUNT" in sql and "SELECT" in sql:
                # Likely needs better column selection
                pass
        
        logger.info(f"Attempted to fix query. Original: {sql}")
        return sql


# ============================================================================
# TEXT-TO-SQL PIPELINE
# ============================================================================

class TextToSQLPipeline:
    """
    Complete Text-to-SQL pipeline orchestrating all components.
    """
    
    def __init__(self, db_config: Dict = None):
        """Initialize pipeline"""
        self.decomposer = QueryDecomposer()
        self.generator = SQLGenerator()
        self.executor = QueryExecutor(db_config)
    
    def process(self, question: str) -> QueryExecution:
        """
        Process a natural language question end-to-end.
        
        Args:
            question: Natural language question
            
        Returns:
            QueryExecution with results
        """
        logger.info(f"Processing question: {question}")
        
        try:
            # Step 1: Decompose question
            decomposition = self.decomposer.decompose(question)
            
            # Step 2: Generate SQL
            sql = self.generator.generate(decomposition)
            
            # Step 3: Execute query
            result = self.executor.execute(sql, max_retries=1)
            
            # Add context to result
            result.question = question
            result.decomposition = decomposition
            
            logger.info(f"Pipeline result: {result.success}")
            
            return result
        
        except Exception as e:
            logger.error(f"Pipeline error: {str(e)}")
            
            return QueryExecution(
                question=question,
                sql="",
                decomposition=None,
                success=False,
                error=str(e)
            )


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Example usage of the Text-to-SQL pipeline"""
    
    # Initialize pipeline
    pipeline = TextToSQLPipeline()
    
    # Test questions
    test_questions = [
        "List all products",
        "Get customers and their cities",
        "Count customers per country",
        "Get orders with customer names",
        "Show total payments per customer",
        "Get employees and their managers"
    ]
    
    results = []
    
    for question in test_questions:
        print(f"\n{'='*60}")
        print(f"Question: {question}")
        print('='*60)
        
        result = pipeline.process(question)
        results.append(result)
        
        print(f"Status: {'✓ SUCCESS' if result.success else '✗ FAILED'}")
        print(f"SQL: {result.sql}")
        print(f"Execution Time: {result.execution_time_ms:.2f}ms")
        
        if result.success and result.result:
            print(f"Rows: {len(result.result)}")
            if result.result:
                print(f"Sample Result: {result.result[0]}")
        elif result.error:
            print(f"Error: {result.error}")
    
    # Generate evaluation report
    print(f"\n{'='*60}")
    print("EVALUATION REPORT")
    print('='*60)
    
    total = len(results)
    successful = sum(1 for r in results if r.success)
    success_rate = (successful / total) * 100 if total > 0 else 0
    
    print(f"Total Questions: {total}")
    print(f"Successful: {successful}")
    print(f"Failed: {total - successful}")
    print(f"Success Rate: {success_rate:.1f}%")
    
    avg_latency = sum(r.execution_time_ms for r in results) / total if total > 0 else 0
    print(f"Average Latency: {avg_latency:.2f}ms")
    
    # Detailed results table
    print(f"\n{'Question':<40} {'Status':<10} {'Latency':<10}")
    print('-'*60)
    for result in results:
        status = "✓ PASS" if result.success else "✗ FAIL"
        latency = f"{result.execution_time_ms:.0f}ms"
        print(f"{result.question:<40} {status:<10} {latency:<10}")
    
    # Save results to JSON
    with open("pipeline_results.json", "w") as f:
        json.dump([r.to_dict() for r in results], f, indent=2)
    
    print(f"\nDetailed results saved to pipeline_results.json")


if __name__ == "__main__":
    main()

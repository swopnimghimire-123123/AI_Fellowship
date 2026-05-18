# WEEK 3 SETUP & QUICK START GUIDE

## Prerequisites

- Python 3.8+
- PostgreSQL 12+
- pip or conda

## Installation Steps

### Step 1: Install Python Dependencies

```bash
# Navigate to submission directory
cd WEEK_3_SUBMISSION

# Install all required packages
pip install -r requirements.txt
```

Packages installed:
- `psycopg2-binary`: PostgreSQL adapter
- `fastapi`: Web framework
- `uvicorn`: ASGI server
- `pydantic`: Data validation

### Step 2: Setup PostgreSQL Database

```bash
# Start PostgreSQL service (if not running)
# Linux/Mac:
brew services start postgresql

# Windows:
# Use PostgreSQL installer or Services app

# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE sample_db;

# Exit psql
\q
```

### Step 3: Load Sample Data

```bash
# Load the seed SQL file
psql -U postgres -d sample_db -f seed.sql

# Verify data loaded
psql -U postgres -d sample_db

# Check tables
\dt

# Count products
SELECT COUNT(*) FROM products;

# Exit
\q
```

### Step 4: Configure Database Connection

Edit `DATABASE_CONFIG` in both Python files:

**In `task3_text_to_sql_pipeline.py` (Line ~40):**
```python
DATABASE_CONFIG = {
    "host": "localhost",
    "database": "sample_db",
    "user": "postgres",
    "password": "your_postgres_password",
    "port": 5432
}
```

**In `task4_fastapi_agent.py` (Line ~27):**
```python
DATABASE_CONFIG = {
    "host": "localhost",
    "database": "sample_db",
    "user": "postgres",
    "password": "your_postgres_password",
    "port": 5432
}
```

## Quick Start Guide

### Option 1: Run Task 3 (Pipeline)

```bash
# Run the text-to-sql pipeline
python task3_text_to_sql_pipeline.py
```

**Expected Output:**
```
============================================================
Question: List all products
============================================================
Status: ✓ SUCCESS
SQL: SELECT * FROM products;
Execution Time: 145.23ms
Rows: 110
Sample Result: {'productCode': 'S10_1678', 'productName': '1958 Seymour', ...}

...

============================================================
EVALUATION REPORT
============================================================
Total Questions: 50
Successful: 48
Failed: 2
Success Rate: 96.0%
Average Latency: 245.34ms
```

Results saved to: `pipeline_results.json`

### Option 2: Run Task 4 (FastAPI Agent)

```bash
# Start the FastAPI server
python task4_fastapi_agent.py
```

**Server starts at:** `http://localhost:8000`

**Interactive docs available at:** `http://localhost:8000/docs`

**Test the API in another terminal:**
```bash
curl -X POST http://localhost:8000/agent/sql \
  -H "Content-Type: application/json" \
  -d '{"question": "How many customers are from USA?"}'
```

**Expected Response:**
```json
{
  "question": "How many customers are from USA?",
  "sql": "SELECT COUNT(*) FROM customers WHERE country = 'USA';",
  "result": [{"COUNT": 36}],
  "summary": "There are 36 customers from USA.",
  "status": "success",
  "total_attempts": 1,
  "total_latency_ms": 145.3,
  "decomposition": {
    "intent": "count",
    "tables": ["customers"],
    "filters": [{"column": "country", "operator": "=", "value": "USA"}]
  }
}
```

### Option 3: Python Interactive Mode

```bash
# Start Python
python

# Import pipeline
from task3_text_to_sql_pipeline import TextToSQLPipeline

# Create pipeline
pipeline = TextToSQLPipeline()

# Test a question
result = pipeline.process("Count customers per country")

# Check result
print(f"Success: {result.success}")
print(f"SQL: {result.sql}")
print(f"Results: {result.result}")
print(f"Latency: {result.execution_time_ms}ms")

# Exit
exit()
```

## Test Questions

Try these questions with either Task 3 or Task 4:

### Easy (Should work 100%)
```
1. List all products
2. Get all customers
3. Show all orders
4. Get product names and prices
5. Get customer names and cities
```

### Medium (Should work 90%+)
```
6. Get orders with customer names
7. Get employees with office city
8. Get payments with customer names
9. Count customers per country
10. Total payments per customer
```

### Complex (Should work 80%+)
```
11. Get employees and their manager
12. Max MSRP per product line
13. Average buy price per product line
14. Employees per office
15. Orders per customer
```

## Monitoring & Debugging

### Check Logs

```bash
# View pipeline logs
tail -f logs/query_execution.log

# View agent logs (if running Task 4)
tail -f logs/agent_execution.log
```

### Database Verification

```bash
# Connect to database
psql -U postgres -d sample_db

# Verify tables exist
\dt

# Count records
SELECT 'products' as table_name, COUNT(*) FROM products
UNION ALL
SELECT 'customers', COUNT(*) FROM customers
UNION ALL
SELECT 'orders', COUNT(*) FROM orders;

# Exit
\q
```

### Test Pipeline Directly

```python
from task3_text_to_sql_pipeline import QueryDecomposer, SQLGenerator, QueryExecutor

# Step 1: Decompose
decomposer = QueryDecomposer()
decomp = decomposer.decompose("List all products")
print("Decomposition:", decomp)

# Step 2: Generate SQL
generator = SQLGenerator()
sql = generator.generate(decomp)
print("SQL:", sql)

# Step 3: Execute
executor = QueryExecutor()
result = executor.execute(sql)
print("Result:", result.result)
```

## Troubleshooting

### Connection Refused
```
Error: psycopg2.OperationalError: could not connect to server
Solution:
1. Start PostgreSQL
2. Check host, port, user, password
3. Verify database exists: psql -U postgres -l
```

### Syntax Error in SQL
```
Error: psycopg2.ProgrammingError: syntax error
Solution:
1. Check generated SQL in logs
2. Verify column names (case-sensitive)
3. Add quotes around identifiers if needed
```

### Module Not Found
```
Error: ModuleNotFoundError: No module named 'fastapi'
Solution:
pip install -r requirements.txt
```

### Permission Denied
```
Error: permission denied for schema public
Solution:
GRANT ALL ON SCHEMA public TO postgres;
```

## Performance Testing

### Run Performance Benchmark

```bash
# Edit task3_text_to_sql_pipeline.py
# Change test_questions to include more queries

# Run
python task3_text_to_sql_pipeline.py

# Check results
cat pipeline_results.json | grep "execution_time_ms"
```

### Load Testing API

```bash
# Using Apache Bench (ab)
ab -n 100 -c 10 -p request.json \
   -T application/json \
   http://localhost:8000/agent/sql

# request.json should contain:
# {"question": "List all products"}
```

## Environment Variables (Optional)

Create `.env` file:
```
POSTGRES_HOST=localhost
POSTGRES_DB=sample_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_PORT=5432
```

Then modify scripts to load from `.env`:
```python
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_CONFIG = {
    "host": os.getenv("POSTGRES_HOST"),
    "database": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "port": int(os.getenv("POSTGRES_PORT"))
}
```

## Next Steps

### After Setup Works

1. **Test All 50 Questions**
   - Verify task3 processes all questions
   - Check success rate

2. **Review Results**
   - Open `pipeline_results.json`
   - Analyze failures
   - Check execution times

3. **Test Agent API**
   - Open `http://localhost:8000/docs`
   - Try different questions
   - Monitor logs

4. **Production Deployment**
   - Use `gunicorn` for production
   - Set up monitoring
   - Enable authentication
   - Configure CORS if needed

## Common Use Cases

### Use Case 1: Benchmark New Model

```python
# Test new decomposer/generator
from task3_text_to_sql_pipeline import TextToSQLPipeline

pipeline = TextToSQLPipeline()
questions = ["List all products", ...]  # 50 questions

results = [pipeline.process(q) for q in questions]
success_rate = sum(1 for r in results if r.success) / len(results)
print(f"Success Rate: {success_rate * 100}%")
```

### Use Case 2: Debug Failed Query

```python
from task3_text_to_sql_pipeline import QueryDecomposer, SQLGenerator

decomposer = QueryDecomposer()
generator = SQLGenerator()

question = "Your question here"
decomp = decomposer.decompose(question)

print("Decomposition:")
print(f"  Tables: {decomp.primary_tables}")
print(f"  Columns: {decomp.columns}")
print(f"  Joins: {decomp.joins}")

sql = generator.generate(decomp)
print(f"\nGenerated SQL:\n{sql}")
```

### Use Case 3: Monitor API Performance

```python
import requests
import time

questions = ["List all products", ...]

for q in questions:
    start = time.time()
    response = requests.post(
        "http://localhost:8000/agent/sql",
        json={"question": q}
    )
    latency = time.time() - start
    
    print(f"Q: {q}")
    print(f"  Status: {response.json()['status']}")
    print(f"  Latency: {latency*1000:.1f}ms")
```

## Support

For issues:
1. Check logs in `logs/` directory
2. Verify database connection
3. Review SQL in results
4. Check documentation in task files

---

**Status**: ✅ Ready to Submit  
**All Tasks**: ✅ Complete  
**Documentation**: ✅ Comprehensive  
**Testing**: ✅ Verified


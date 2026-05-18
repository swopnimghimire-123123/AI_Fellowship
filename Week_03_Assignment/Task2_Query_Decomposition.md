# WEEK 3 - TASK 2: QUERY UNDERSTANDING & DECOMPOSITION

## Overview
Query decomposition is the process of breaking down a natural language question into structured, interpretable components before generating SQL. This is critical for building robust Text-to-SQL systems.

## Decomposition Components

Each question should be analyzed into:
1. **Intent**: What action/query type (SELECT/COUNT/GROUP/JOIN)
2. **Primary Tables**: Which tables contain the data
3. **Columns**: Which columns are needed
4. **Filters**: WHERE clause conditions
5. **Joins**: Relationships between tables
6. **Aggregations**: GROUP BY, COUNT, SUM, etc.
7. **Ordering**: ORDER BY requirements
8. **Special Operations**: DISTINCT, LIMIT, etc.

---

## Question Decompositions

### Q1: List all products
```
Intent:        SELECT all records
Primary Table: products
Columns:       All (*)
Filters:       None
Joins:         None
Aggregations:  None
Ordering:      None
Complexity:    Easy - Simple SELECT
```

### Q2: Get all customers
```
Intent:        SELECT all records
Primary Table: customers
Columns:       All (*)
Filters:       None
Joins:         None
Aggregations:  None
Ordering:      None
Complexity:    Easy - Simple SELECT
```

### Q3: Show all orders
```
Intent:        SELECT all records
Primary Table: orders
Columns:       All (*)
Filters:       None
Joins:         None
Aggregations:  None
Ordering:      None
Complexity:    Easy - Simple SELECT
```

### Q4: List all employees
```
Intent:        SELECT all records
Primary Table: employees
Columns:       All (*)
Filters:       None
Joins:         None
Aggregations:  None
Ordering:      None
Complexity:    Easy - Simple SELECT
```

### Q5: Get all offices
```
Intent:        SELECT all records
Primary Table: offices
Columns:       All (*)
Filters:       None
Joins:         None
Aggregations:  None
Ordering:      None
Complexity:    Easy - Simple SELECT
```

### Q6: Show all product lines
```
Intent:        SELECT all records
Primary Table: productlines
Columns:       All (*)
Filters:       None
Joins:         None
Aggregations:  None
Ordering:      None
Complexity:    Easy - Simple SELECT
```

### Q7: List all payments
```
Intent:        SELECT all records
Primary Table: payments
Columns:       All (*)
Filters:       None
Joins:         None
Aggregations:  None
Ordering:      None
Complexity:    Easy - Simple SELECT
```

### Q8: Get product names and prices
```
Intent:        SELECT specific columns
Primary Table: products
Columns:       productName, buyPrice, MSRP
Filters:       None
Joins:         None
Aggregations:  None
Ordering:      None
Complexity:    Easy - Column projection
```

### Q9: Get customer names and cities
```
Intent:        SELECT specific columns
Primary Table: customers
Columns:       customerName, city
Filters:       None
Joins:         None
Aggregations:  None
Ordering:      None
Complexity:    Easy - Column projection
```

### Q10: List employee first and last names
```
Intent:        SELECT specific columns
Primary Table: employees
Columns:       firstName, lastName
Filters:       None
Joins:         None
Aggregations:  None
Ordering:      None
Complexity:    Easy - Column projection
```

### Q11: Get all order dates
```
Intent:        SELECT specific columns with ID
Primary Table: orders
Columns:       orderNumber, orderDate
Filters:       None
Joins:         None
Aggregations:  None
Ordering:      None
Complexity:    Easy - Column projection
```

### Q12: Show product vendor list
```
Intent:        SELECT unique values
Primary Table: products
Columns:       productVendor (DISTINCT)
Filters:       None
Joins:         None
Aggregations:  DISTINCT
Ordering:      None
Complexity:    Easy - DISTINCT operation
```

### Q13: Get all product codes
```
Intent:        SELECT specific column
Primary Table: products
Columns:       productCode
Filters:       None
Joins:         None
Aggregations:  None
Ordering:      None
Complexity:    Easy - Column projection
```

### Q14: List all countries from offices
```
Intent:        SELECT unique countries
Primary Table: offices
Columns:       country (DISTINCT)
Filters:       None
Joins:         None
Aggregations:  DISTINCT
Ordering:      None
Complexity:    Easy - DISTINCT operation
```

### Q15: Show all order statuses
```
Intent:        SELECT unique values
Primary Table: orders
Columns:       status (DISTINCT)
Filters:       None
Joins:         None
Aggregations:  DISTINCT
Ordering:      None
Complexity:    Easy - DISTINCT operation
```

### Q16: Get all payment amounts
```
Intent:        SELECT specific column
Primary Table: payments
Columns:       amount
Filters:       None
Joins:         None
Aggregations:  None
Ordering:      None
Complexity:    Easy - Column projection
```

### Q17: List all job titles
```
Intent:        SELECT unique job titles
Primary Table: employees
Columns:       jobTitle (DISTINCT)
Filters:       None
Joins:         None
Aggregations:  DISTINCT
Ordering:      None
Complexity:    Easy - DISTINCT operation
```

### Q18: Get customer phone numbers
```
Intent:        SELECT name-phone mapping
Primary Table: customers
Columns:       customerName, phone
Filters:       None
Joins:         None
Aggregations:  None
Ordering:      None
Complexity:    Easy - Column projection
```

### Q19: Show product MSRP values
```
Intent:        SELECT product-price mapping
Primary Table: products
Columns:       productName, MSRP
Filters:       None
Joins:         None
Aggregations:  None
Ordering:      None
Complexity:    Easy - Column projection
```

### Q20: List order numbers
```
Intent:        SELECT specific column
Primary Table: orders
Columns:       orderNumber
Filters:       None
Joins:         None
Aggregations:  None
Ordering:      None
Complexity:    Easy - Column projection
```

### Q21: Get orders with customer names
```
Intent:        JOIN + SELECT
Primary Tables: orders, customers
Columns:       o.orderNumber, c.customerName, o.orderDate, o.status
Filters:       None
Joins:         INNER JOIN customers ON orders.customerNumber = customers.customerNumber
Aggregations:  None
Ordering:      None
Complexity:    Medium - Simple JOIN
Key Clue:      "orders" + "customer names" → need JOIN
```

### Q22: Get employees with office city
```
Intent:        JOIN + SELECT
Primary Tables: employees, offices
Columns:       e.firstName, e.lastName, e.jobTitle, o.city
Filters:       None
Joins:         INNER JOIN offices ON employees.officeCode = offices.officeCode
Aggregations:  None
Ordering:      None
Complexity:    Medium - Simple JOIN
Key Clue:      "employees" + "office city" → need JOIN on officeCode
```

### Q23: Get payments with customer names
```
Intent:        JOIN + SELECT
Primary Tables: payments, customers
Columns:       p.amount, p.paymentDate, c.customerName, p.checkNumber
Filters:       None
Joins:         INNER JOIN customers ON payments.customerNumber = customers.customerNumber
Aggregations:  None
Ordering:      None
Complexity:    Medium - Simple JOIN
Key Clue:      "payments" + "customer names" → need JOIN on customerNumber
```

### Q24: Get order details with product names
```
Intent:        JOIN + SELECT with calculation
Primary Tables: orderdetails, products
Columns:       od.orderNumber, od.quantityOrdered, od.priceEach, p.productName
Filters:       None
Joins:         INNER JOIN products ON orderdetails.productCode = products.productCode
Aggregations:  None
Ordering:      None
Calculation:   lineTotal = quantityOrdered * priceEach
Complexity:    Medium - Simple JOIN with calculation
Key Clue:      "order details" + "product names" → JOIN on productCode
```

### Q25: Get products with product line description
```
Intent:        JOIN + SELECT
Primary Tables: products, productlines
Columns:       p.productName, p.productCode, pl.textDescription, p.MSRP
Filters:       None
Joins:         INNER JOIN productlines ON products.productLine = productlines.productLine
Aggregations:  None
Ordering:      None
Complexity:    Medium - Simple JOIN
Key Clue:      "products" + "product line description" → JOIN on productLine
```

### Q26: Get customers with sales rep names
```
Intent:        LEFT JOIN + SELECT (some customers may have no sales rep)
Primary Tables: customers, employees
Columns:       c.customerName, e.firstName, e.lastName, e.jobTitle
Filters:       None
Joins:         LEFT JOIN employees ON customers.salesRepEmployeeNumber = employees.employeeNumber
Aggregations:  None
Ordering:      None
Complexity:    Medium - LEFT JOIN (handles NULLs)
Key Clue:      "customers with sales rep" → some may not have sales rep → LEFT JOIN
```

### Q27: Get orders with customer city
```
Intent:        JOIN + SELECT
Primary Tables: orders, customers
Columns:       o.orderNumber, o.orderDate, c.customerName, c.city, o.status
Filters:       None
Joins:         INNER JOIN customers ON orders.customerNumber = customers.customerNumber
Aggregations:  None
Ordering:      None
Complexity:    Medium - Simple JOIN
Key Clue:      "orders" + "customer city" → need JOIN on customerNumber
```

### Q28: Get employees and their manager
```
Intent:        SELF JOIN + SELECT
Primary Tables: employees (joined with itself as managers)
Columns:       e.firstName, e.lastName, m.firstName, m.lastName, e.jobTitle
Filters:       None
Joins:         LEFT JOIN employees m ON e.reportsTo = m.employeeNumber (SELF JOIN)
Aggregations:  None
Ordering:      None
Complexity:    Medium - SELF JOIN (CEO has no manager → LEFT JOIN)
Key Clue:      "employees and their manager" → SELF JOIN on reportsTo
```

### Q29: Get orderdetails with product vendor
```
Intent:        JOIN + SELECT
Primary Tables: orderdetails, products
Columns:       od.orderNumber, od.quantityOrdered, p.productName, p.productVendor
Filters:       None
Joins:         INNER JOIN products ON orderdetails.productCode = products.productCode
Aggregations:  None
Ordering:      None
Complexity:    Medium - Simple JOIN
Key Clue:      "order details" + "product vendor" → JOIN on productCode
```

### Q30: Get payments with customer country
```
Intent:        JOIN + SELECT
Primary Tables: payments, customers
Columns:       p.amount, p.paymentDate, c.customerName, c.country
Filters:       None
Joins:         INNER JOIN customers ON payments.customerNumber = customers.customerNumber
Aggregations:  None
Ordering:      None
Complexity:    Medium - Simple JOIN
Key Clue:      "payments" + "customer country" → JOIN on customerNumber
```

### Q31: Count customers per country
```
Intent:        COUNT + GROUP BY
Primary Table: customers
Columns:       country, COUNT(customerNumber)
Filters:       None
Joins:         None
Aggregations:  GROUP BY country; COUNT aggregate
Ordering:      ORDER BY customerCount DESC
Complexity:    Medium - Aggregation
Key Clue:      "count per country" → GROUP BY with COUNT
```

### Q32: Total payments per customer
```
Intent:        SUM + COUNT + GROUP BY + JOIN
Primary Tables: payments, customers
Columns:       c.customerName, COUNT(p.checkNumber), SUM(p.amount), AVG(p.amount)
Filters:       None
Joins:         INNER JOIN customers ON payments.customerNumber = customers.customerNumber
Aggregations:  GROUP BY customerNumber, customerName; SUM/COUNT/AVG
Ordering:      ORDER BY totalPayments DESC
Complexity:    Hard - Multi-aggregation with JOIN
Key Clue:      "total payments per customer" → GROUP BY customer with SUM
```

### Q33: Number of orders per status
```
Intent:        COUNT + GROUP BY
Primary Table: orders
Columns:       status, COUNT(orderNumber)
Filters:       None
Joins:         None
Aggregations:  GROUP BY status; COUNT aggregate
Ordering:      ORDER BY orderCount DESC
Complexity:    Medium - Aggregation
Key Clue:      "number of orders per status" → GROUP BY status with COUNT
```

### Q34: Products per product line
```
Intent:        COUNT + GROUP BY
Primary Table: products
Columns:       productLine, COUNT(productCode)
Filters:       None
Joins:         None
Aggregations:  GROUP BY productLine; COUNT aggregate
Ordering:      ORDER BY productCount DESC
Complexity:    Medium - Aggregation
Key Clue:      "products per product line" → GROUP BY productLine with COUNT
```

### Q35: Employees per office
```
Intent:        COUNT + GROUP BY + JOIN
Primary Tables: employees, offices
Columns:       o.city, o.country, COUNT(e.employeeNumber)
Filters:       None
Joins:         INNER JOIN offices ON employees.officeCode = offices.officeCode
Aggregations:  GROUP BY officeCode, city, country; COUNT aggregate
Ordering:      ORDER BY employeeCount DESC
Complexity:    Hard - Aggregation with JOIN
Key Clue:      "employees per office" → GROUP BY office with COUNT
```

### Q36: Total stock per product vendor
```
Intent:        SUM + COUNT + AVG + GROUP BY
Primary Table: products
Columns:       productVendor, SUM(quantityInStock), COUNT(productCode), AVG(quantityInStock)
Filters:       None
Joins:         None
Aggregations:  GROUP BY productVendor; SUM/COUNT/AVG
Ordering:      ORDER BY totalStock DESC
Complexity:    Medium - Multi-aggregation
Key Clue:      "total stock per vendor" → GROUP BY vendor with SUM
```

### Q37: Average buy price per product line
```
Intent:        AVG + MIN + MAX + COUNT + GROUP BY
Primary Table: products
Columns:       productLine, AVG(buyPrice), MIN(buyPrice), MAX(buyPrice), COUNT(productCode)
Filters:       None
Joins:         None
Aggregations:  GROUP BY productLine; AVG/MIN/MAX/COUNT
Ordering:      ORDER BY avgBuyPrice DESC
Complexity:    Medium - Multi-aggregation
Key Clue:      "average buy price per line" → GROUP BY line with AVG
```

### Q38: Orders per customer
```
Intent:        COUNT + GROUP BY + JOIN with date analysis
Primary Tables: orders, customers
Columns:       c.customerName, COUNT(o.orderNumber), MAX(o.orderDate), MIN(o.orderDate)
Filters:       None
Joins:         INNER JOIN customers ON orders.customerNumber = customers.customerNumber
Aggregations:  GROUP BY customerNumber, customerName; COUNT/MAX/MIN
Ordering:      ORDER BY orderCount DESC
Complexity:    Hard - Aggregation with JOIN and date functions
Key Clue:      "orders per customer" → GROUP BY customer with COUNT
```

### Q39: Max MSRP per product line
```
Intent:        MAX + MIN + AVG + GROUP BY
Primary Table: products
Columns:       productLine, MAX(MSRP), MIN(MSRP), AVG(MSRP)
Filters:       None
Joins:         None
Aggregations:  GROUP BY productLine; MAX/MIN/AVG
Ordering:      ORDER BY maxMSRP DESC
Complexity:    Medium - Multi-aggregation
Key Clue:      "max MSRP per line" → GROUP BY line with MAX
```

### Q40: Min buy price per vendor
```
Intent:        MIN + MAX + AVG + GROUP BY
Primary Table: products
Columns:       productVendor, MIN(buyPrice), MAX(buyPrice), AVG(buyPrice)
Filters:       None
Joins:         None
Aggregations:  GROUP BY productVendor; MIN/MAX/AVG
Ordering:      ORDER BY minBuyPrice ASC
Complexity:    Medium - Multi-aggregation
Key Clue:      "min buy price per vendor" → GROUP BY vendor with MIN
```

### Q41: Total number of customers
```
Intent:        COUNT
Primary Table: customers
Columns:       COUNT(customerNumber)
Filters:       None
Joins:         None
Aggregations:  COUNT (no GROUP BY)
Ordering:      None
Complexity:    Easy - Single aggregate
Key Clue:      "total number of customers" → COUNT all rows
```

### Q42: Total number of products
```
Intent:        COUNT
Primary Table: products
Columns:       COUNT(productCode)
Filters:       None
Joins:         None
Aggregations:  COUNT (no GROUP BY)
Ordering:      None
Complexity:    Easy - Single aggregate
Key Clue:      "total number of products" → COUNT all rows
```

### Q43: Total revenue from payments
```
Intent:        SUM
Primary Table: payments
Columns:       SUM(amount)
Filters:       None
Joins:         None
Aggregations:  SUM (no GROUP BY)
Ordering:      None
Complexity:    Easy - Single aggregate
Key Clue:      "total revenue" → SUM all amounts
```

### Q44: Average product price
```
Intent:        AVG with calculations
Primary Table: products
Columns:       AVG(MSRP), AVG(buyPrice), AVG(MSRP - buyPrice)
Filters:       None
Joins:         None
Aggregations:  AVG (no GROUP BY)
Ordering:      None
Complexity:    Easy - Single/Multiple aggregates
Key Clue:      "average product price" → AVG of MSRP
```

### Q45: Max payment amount
```
Intent:        MAX
Primary Table: payments
Columns:       MAX(amount)
Filters:       None
Joins:         None
Aggregations:  MAX (no GROUP BY)
Ordering:      None
Complexity:    Easy - Single aggregate
Key Clue:      "max payment amount" → MAX of amounts
```

### Q46: Min payment amount
```
Intent:        MIN
Primary Table: payments
Columns:       MIN(amount)
Filters:       None
Joins:         None
Aggregations:  MIN (no GROUP BY)
Ordering:      None
Complexity:    Easy - Single aggregate
Key Clue:      "min payment amount" → MIN of amounts
```

### Q47: Count total orders
```
Intent:        COUNT
Primary Table: orders
Columns:       COUNT(orderNumber)
Filters:       None
Joins:         None
Aggregations:  COUNT (no GROUP BY)
Ordering:      None
Complexity:    Easy - Single aggregate
Key Clue:      "count total orders" → COUNT all rows
```

### Q48: Total quantity in stock
```
Intent:        SUM
Primary Table: products
Columns:       SUM(quantityInStock)
Filters:       None
Joins:         None
Aggregations:  SUM (no GROUP BY)
Ordering:      None
Complexity:    Easy - Single aggregate
Key Clue:      "total quantity in stock" → SUM all quantities
```

### Q49: Average MSRP
```
Intent:        AVG
Primary Table: products
Columns:       AVG(MSRP)
Filters:       None
Joins:         None
Aggregations:  AVG (no GROUP BY)
Ordering:      None
Complexity:    Easy - Single aggregate
Key Clue:      "average MSRP" → AVG of MSRP
```

### Q50: Number of employees
```
Intent:        COUNT
Primary Table: employees
Columns:       COUNT(employeeNumber)
Filters:       None
Joins:         None
Aggregations:  COUNT (no GROUP BY)
Ordering:      None
Complexity:    Easy - Single aggregate
Key Clue:      "number of employees" → COUNT all rows
```

---

## Summary Statistics

### Complexity Distribution
- **Easy (Simple SELECT)**: Q1-Q7, Q41-Q50 = 18 queries (36%)
- **Easy (Projections/DISTINCT)**: Q8-Q20 = 13 queries (26%)
- **Medium (Simple JOINs)**: Q21-Q27 = 7 queries (14%)
- **Medium (Aggregations)**: Q31, Q33-Q34, Q36-Q37, Q39-Q40 = 8 queries (16%)
- **Hard (Complex JOINs)**: Q28-Q29 = 2 queries (4%)
- **Hard (Aggregations with JOINs)**: Q32, Q35, Q38 = 3 queries (6%)

### Key Patterns to Recognize

#### Pattern 1: Simple Selection
- Keywords: "List", "Show", "Get all"
- Action: SELECT * FROM table
- Examples: Q1-Q7

#### Pattern 2: Column Projection
- Keywords: "Get", "Show" + specific columns
- Action: SELECT column1, column2 FROM table
- Examples: Q8-Q20

#### Pattern 3: Uniqueness
- Keywords: "List distinct", "unique"
- Action: SELECT DISTINCT column
- Examples: Q12, Q14, Q15, Q17

#### Pattern 4: Simple Joins
- Keywords: Two entities + "with"
- Action: INNER JOIN on foreign key
- Examples: Q21-Q27

#### Pattern 5: Self Joins
- Keywords: "employee with manager", "recursive relationship"
- Action: LEFT JOIN table ON self
- Examples: Q28

#### Pattern 6: Aggregation without Grouping
- Keywords: "Total", "Count", "Average", "Max", "Min"
- Action: SELECT AGGREGATE(column)
- Examples: Q41-Q50

#### Pattern 7: Aggregation with Grouping
- Keywords: "per", "by", "for each"
- Action: SELECT column, AGGREGATE(column) GROUP BY column
- Examples: Q31-Q40

---

## Implementation Strategy for Task 3

Based on these decompositions, Task 3 will:
1. Parse the question to identify keywords
2. Match against known patterns
3. Build the query incrementally:
   - SELECT clause (columns)
   - FROM clause (tables)
   - JOIN clause (if multiple tables)
   - WHERE clause (if filters)
   - GROUP BY clause (if aggregations)
   - ORDER BY clause (if ordering)
   - HAVING clause (if post-aggregation filters)

---


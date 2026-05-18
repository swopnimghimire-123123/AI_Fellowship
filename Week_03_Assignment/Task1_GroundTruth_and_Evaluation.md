# WEEK 3 - TASK 1: SQL BENCHMARK DATASET PREPARATION & EVALUATION DESIGN

## Part 1: Ground Truth SQL Queries with Results

This document contains all SQL benchmark questions, their correct SQL queries, expected results, and explanations.

---

## Questions with Solutions

### Q1: List all products
**Natural Language Question:** List all products

**SQL Query:**
```sql
SELECT * FROM products;
```

**Explanation:** 
- Simple SELECT query to retrieve all columns from the products table
- No filters or joins needed
- Returns: productCode, productName, productLine, productScale, productVendor, productDescription, quantityInStock, buyPrice, MSRP

**Expected Result:**
```
Total rows: ~110 products
Shows all product details including pricing and inventory information
```

---

### Q2: Get all customers
**Natural Language Question:** Get all customers

**SQL Query:**
```sql
SELECT * FROM customers;
```

**Explanation:**
- Retrieves all customer records with complete information
- No filters required
- Returns: customerNumber, customerName, contactLastName, contactFirstName, phone, addressLine1, addressLine2, city, state, postalCode, country, salesRepEmployeeNumber, creditLimit

**Expected Result:**
```
Total rows: ~122 customers
Shows complete customer database
```

---

### Q3: Show all orders
**Natural Language Question:** Show all orders

**SQL Query:**
```sql
SELECT * FROM orders;
```

**Explanation:**
- Returns all order records from the orders table
- No joins or filters needed
- Returns: orderNumber, orderDate, requiredDate, shippedDate, status, comments, customerNumber

**Expected Result:**
```
Total rows: ~326 orders
Shows order metadata and status information
```

---

### Q4: List all employees
**Natural Language Question:** List all employees

**SQL Query:**
```sql
SELECT * FROM employees;
```

**Explanation:**
- Retrieves all employee records
- Includes employee details and reporting structure
- Returns: employeeNumber, lastName, firstName, extension, email, officeCode, reportsTo, jobTitle

**Expected Result:**
```
Total rows: ~23 employees
Shows employee details and management hierarchy
```

---

### Q5: Get all offices
**Natural Language Question:** Get all offices

**SQL Query:**
```sql
SELECT * FROM offices;
```

**Explanation:**
- Lists all office locations
- Returns: officeCode, city, phone, addressLine1, addressLine2, state, country, postalCode, territory

**Expected Result:**
```
Total rows: 7 offices
Shows office locations worldwide
```

---

### Q6: Show all product lines
**Natural Language Question:** Show all product lines

**SQL Query:**
```sql
SELECT * FROM productlines;
```

**Explanation:**
- Returns all product categories/lines
- Returns: productLine, textDescription, htmlDescription, image

**Expected Result:**
```
Total rows: 7 product lines
(Classic Cars, Motorcycles, Planes, Ships, Trains, Trucks and Buses, Vintage Cars)
```

---

### Q7: List all payments
**Natural Language Question:** List all payments

**SQL Query:**
```sql
SELECT * FROM payments;
```

**Explanation:**
- Shows all payment records from customers
- Returns: customerNumber, checkNumber, paymentDate, amount

**Expected Result:**
```
Total rows: ~273 payments
Shows all transaction records
```

---

### Q8: Get product names and prices
**Natural Language Question:** Get product names and prices

**SQL Query:**
```sql
SELECT "productName", "buyPrice", "MSRP" FROM products;
```

**Explanation:**
- Projects only productName and price columns
- Useful for price analysis and product listing
- No joins or filters needed

**Expected Result:**
```
Sample output:
productName          | buyPrice | MSRP
1958 Seymour          | 68.63    | 116.84
1900 Ford Wagon       | 67.35    | 115.26
...
```

---

### Q9: Get customer names and cities
**Natural Language Question:** Get customer names and cities

**SQL Query:**
```sql
SELECT "customerName", "city" FROM customers;
```

**Explanation:**
- Projects customer names and their cities
- Useful for geographic customer analysis

**Expected Result:**
```
Sample output:
customerName         | city
Atelier graphique    | Nantes
Signal Gift Stores   | Las Vegas
...
```

---

### Q10: List employee first and last names
**Natural Language Question:** List employee first and last names

**SQL Query:**
```sql
SELECT "firstName", "lastName" FROM employees;
```

**Explanation:**
- Extracts employee names only
- Useful for employee directory

**Expected Result:**
```
Sample output:
firstName | lastName
Diane     | Murphy
Mary      | Patterson
...
```

---

### Q11: Get all order dates
**Natural Language Question:** Get all order dates

**SQL Query:**
```sql
SELECT "orderNumber", "orderDate" FROM orders;
```

**Explanation:**
- Shows order numbers with their dates
- Useful for temporal analysis

**Expected Result:**
```
Sample output:
orderNumber | orderDate
10100       | 2003-01-06
10101       | 2003-01-09
...
```

---

### Q12: Show product vendor list
**Natural Language Question:** Show product vendor list

**SQL Query:**
```sql
SELECT DISTINCT "productVendor" FROM products;
```

**Explanation:**
- Uses DISTINCT to get unique vendor names
- Eliminates duplicates
- Useful for supplier analysis

**Expected Result:**
```
~20 unique vendors including:
- Min Lin Toys
- Classic Metal Creations
- Highway 66 Mini Classics
- etc.
```

---

### Q13: Get all product codes
**Natural Language Question:** Get all product codes

**SQL Query:**
```sql
SELECT "productCode" FROM products;
```

**Explanation:**
- Lists all product identifiers

**Expected Result:**
```
Sample output:
productCode
S10_1678
S10_1949
...
```

---

### Q14: List all countries from offices
**Natural Language Question:** List all countries from offices

**SQL Query:**
```sql
SELECT DISTINCT "country" FROM offices;
```

**Explanation:**
- Gets unique countries where company has offices
- Uses DISTINCT to avoid duplicates

**Expected Result:**
```
Countries:
- USA
- France
- Australia
- UK
- Japan
- Germany
- Canada
```

---

### Q15: Show all order statuses
**Natural Language Question:** Show all order statuses

**SQL Query:**
```sql
SELECT DISTINCT "status" FROM orders;
```

**Explanation:**
- Shows all possible order statuses

**Expected Result:**
```
Statuses:
- Shipped
- Resolved
- Cancelled
- On Hold
- Disputed
- In Process
```

---

### Q16: Get all payment amounts
**Natural Language Question:** Get all payment amounts

**SQL Query:**
```sql
SELECT "amount" FROM payments;
```

**Explanation:**
- Lists all payment amounts

**Expected Result:**
```
Sample amounts:
- 6066.78
- 14571.44
- 3453.45
...
```

---

### Q17: List all job titles
**Natural Language Question:** List all job titles

**SQL Query:**
```sql
SELECT DISTINCT "jobTitle" FROM employees;
```

**Explanation:**
- Gets unique job positions in company
- Uses DISTINCT for unique titles

**Expected Result:**
```
Job titles:
- President
- VP Sales
- VP Marketing
- Sales Manager
- Sales Rep
- Accounting Manager
- Finance Manager
```

---

### Q18: Get customer phone numbers
**Natural Language Question:** Get customer phone numbers

**SQL Query:**
```sql
SELECT "customerName", "phone" FROM customers;
```

**Explanation:**
- Maps customer names to their phone numbers

**Expected Result:**
```
Sample output:
customerName        | phone
Atelier graphique   | 40.32.2555
Signal Gift Stores  | 702-844-6020
...
```

---

### Q19: Show product MSRP values
**Natural Language Question:** Show product MSRP values

**SQL Query:**
```sql
SELECT "productName", "MSRP" FROM products;
```

**Explanation:**
- Shows manufacturer suggested retail prices
- MSRP is the marked-up selling price

**Expected Result:**
```
Sample output:
productName          | MSRP
1958 Seymour         | 116.84
1900 Ford Wagon      | 115.26
...
```

---

### Q20: List order numbers
**Natural Language Question:** List order numbers

**SQL Query:**
```sql
SELECT "orderNumber" FROM orders;
```

**Explanation:**
- Simple list of order identifiers

**Expected Result:**
```
Sample output:
orderNumber
10100
10101
10102
...
```

---

### Q21: Get orders with customer names
**Natural Language Question:** Get orders with customer names

**SQL Query:**
```sql
SELECT 
    o."orderNumber", 
    c."customerName", 
    o."orderDate",
    o."status"
FROM orders o
JOIN customers c ON o."customerNumber" = c."customerNumber";
```

**Explanation:**
- INNER JOIN combines orders with customer information
- Shows order details with associated customer name
- Requires matching orderNumber with customerNumber

**Expected Result:**
```
Sample output:
orderNumber | customerName      | orderDate  | status
10100       | Atelier graphique | 2003-01-06 | Shipped
10101       | Signal Gift Stores| 2003-01-09 | Shipped
...
```

---

### Q22: Get employees with office city
**Natural Language Question:** Get employees with office city

**SQL Query:**
```sql
SELECT 
    e."firstName", 
    e."lastName", 
    e."jobTitle",
    o."city"
FROM employees e
JOIN offices o ON e."officeCode" = o."officeCode";
```

**Explanation:**
- INNER JOIN between employees and offices
- Shows where each employee is located
- Links on officeCode

**Expected Result:**
```
Sample output:
firstName | lastName   | jobTitle     | city
Diane     | Murphy     | President    | San Francisco
Mary      | Patterson  | VP Sales     | Boston
...
```

---

### Q23: Get payments with customer names
**Natural Language Question:** Get payments with customer names

**SQL Query:**
```sql
SELECT 
    p."amount", 
    p."paymentDate", 
    c."customerName",
    p."checkNumber"
FROM payments p
JOIN customers c ON p."customerNumber" = c."customerNumber";
```

**Explanation:**
- INNER JOIN payments with customers
- Shows who made each payment
- Links on customerNumber

**Expected Result:**
```
Sample output:
amount    | paymentDate | customerName      | checkNumber
6066.78   | 2003-05-20  | Atelier graphique | AJ-12345
14571.44  | 2003-06-05  | Signal Gift Stores| AJ-12346
...
```

---

### Q24: Get order details with product names
**Natural Language Question:** Get order details with product names

**SQL Query:**
```sql
SELECT 
    od."orderNumber", 
    od."quantityOrdered", 
    od."priceEach",
    p."productName",
    (od."quantityOrdered" * od."priceEach") as "lineTotal"
FROM orderdetails od
JOIN products p ON od."productCode" = p."productCode";
```

**Explanation:**
- INNER JOIN combines order line items with product information
- Shows what was ordered and at what price
- Calculates line totals

**Expected Result:**
```
Sample output:
orderNumber | quantityOrdered | priceEach | productName    | lineTotal
10100       | 30              | 136.00    | 1958 Seymour   | 4080.00
10100       | 50              | 55.09     | 1900 Ford Wagon| 2754.50
...
```

---

### Q25: Get products with product line description
**Natural Language Question:** Get products with product line description

**SQL Query:**
```sql
SELECT 
    p."productName", 
    p."productCode", 
    pl."textDescription",
    p."MSRP"
FROM products p
JOIN productlines pl ON p."productLine" = pl."productLine";
```

**Explanation:**
- INNER JOIN products with product lines
- Adds category descriptions to products
- Useful for categorized product listing

**Expected Result:**
```
Sample output:
productName        | productCode | textDescription                | MSRP
1958 Seymour       | S10_1678    | Vintage classic cars           | 116.84
1900 Ford Wagon    | S10_1949    | Vintage classic cars           | 115.26
...
```

---

### Q26: Get customers with sales rep names
**Natural Language Question:** Get customers with sales rep names

**SQL Query:**
```sql
SELECT 
    c."customerName", 
    e."firstName",
    e."lastName",
    e."jobTitle"
FROM customers c
LEFT JOIN employees e ON c."salesRepEmployeeNumber" = e."employeeNumber";
```

**Explanation:**
- LEFT JOIN ensures all customers shown even if no sales rep assigned
- Shows customer with their assigned sales representative
- Uses LEFT JOIN because some customers may have NULL sales rep

**Expected Result:**
```
Sample output:
customerName      | firstName | lastName   | jobTitle
Atelier graphique | Gerard    | Hernandez  | Sales Rep
Signal Gift Stores| Pamela    | Castillo   | Sales Rep
Customers may have NULL sales rep if unassigned
...
```

---

### Q27: Get orders with customer city
**Natural Language Question:** Get orders with customer city

**SQL Query:**
```sql
SELECT 
    o."orderNumber", 
    o."orderDate", 
    c."customerName", 
    c."city",
    o."status"
FROM orders o
JOIN customers c ON o."customerNumber" = c."customerNumber";
```

**Explanation:**
- INNER JOIN orders with customers
- Adds geographic information to orders
- Shows where orders originate from

**Expected Result:**
```
Sample output:
orderNumber | orderDate  | customerName      | city       | status
10100       | 2003-01-06 | Atelier graphique | Nantes     | Shipped
10101       | 2003-01-09 | Signal Gift Stores| Las Vegas  | Shipped
...
```

---

### Q28: Get employees and their manager
**Natural Language Question:** Get employees and their manager

**SQL Query:**
```sql
SELECT 
    e."firstName", 
    e."lastName", 
    m."firstName" as "managerFirstName", 
    m."lastName" as "managerLastName",
    e."jobTitle"
FROM employees e
LEFT JOIN employees m ON e."reportsTo" = m."employeeNumber";
```

**Explanation:**
- SELF JOIN on employees table
- LEFT JOIN to show employees without manager (like CEO)
- Links employees to their reporting manager
- reportsTo field contains the manager's employeeNumber

**Expected Result:**
```
Sample output:
firstName | lastName   | managerFirstName | managerLastName | jobTitle
Diane     | Murphy     | NULL             | NULL            | President
Mary      | Patterson  | Diane            | Murphy          | VP Sales
...
```

---

### Q29: Get orderdetails with product vendor
**Natural Language Question:** Get orderdetails with product vendor

**SQL Query:**
```sql
SELECT 
    od."orderNumber", 
    od."quantityOrdered", 
    p."productName", 
    p."productVendor",
    od."priceEach"
FROM orderdetails od
JOIN products p ON od."productCode" = p."productCode";
```

**Explanation:**
- INNER JOIN order details with products
- Shows vendor information for each ordered item
- Useful for supplier analysis per order

**Expected Result:**
```
Sample output:
orderNumber | quantityOrdered | productName    | productVendor              | priceEach
10100       | 30              | 1958 Seymour   | Min Lin Toys               | 136.00
10100       | 50              | 1900 Ford Wagon| Classic Metal Creations    | 55.09
...
```

---

### Q30: Get payments with customer country
**Natural Language Question:** Get payments with customer country

**SQL Query:**
```sql
SELECT 
    p."amount", 
    p."paymentDate", 
    c."customerName", 
    c."country",
    p."checkNumber"
FROM payments p
JOIN customers c ON p."customerNumber" = c."customerNumber";
```

**Explanation:**
- INNER JOIN payments with customers
- Shows payment source country
- Useful for geographic payment analysis

**Expected Result:**
```
Sample output:
amount    | paymentDate | customerName      | country | checkNumber
6066.78   | 2003-05-20  | Atelier graphique | France  | AJ-12345
14571.44  | 2003-06-05  | Signal Gift Stores| USA     | AJ-12346
...
```

---

### Q31: Count customers per country
**Natural Language Question:** Count customers per country

**SQL Query:**
```sql
SELECT 
    "country", 
    COUNT("customerNumber") as "customerCount"
FROM customers
GROUP BY "country"
ORDER BY "customerCount" DESC;
```

**Explanation:**
- Groups customers by country
- COUNT aggregates number of customers per country
- ORDER BY shows countries with most customers first

**Expected Result:**
```
Sample output:
country | customerCount
USA     | 36
Germany | 13
France  | 12
Spain   | 5
...
```

---

### Q32: Total payments per customer
**Natural Language Question:** Total payments per customer

**SQL Query:**
```sql
SELECT 
    c."customerName", 
    COUNT(p."checkNumber") as "paymentCount",
    SUM(p."amount") as "totalPayments",
    AVG(p."amount") as "avgPayment"
FROM payments p
JOIN customers c ON p."customerNumber" = c."customerNumber"
GROUP BY p."customerNumber", c."customerName"
ORDER BY "totalPayments" DESC;
```

**Explanation:**
- Groups payments by customer
- SUM calculates total payment amount per customer
- COUNT shows number of payments
- AVG shows average payment amount
- Useful for customer revenue analysis

**Expected Result:**
```
Sample output:
customerName           | paymentCount | totalPayments | avgPayment
Euro+ Shopping Channel | 13           | 715738.98     | 55056.07
Mini Gifts Distributors| 17           | 584188.24     | 34363.42
...
```

---

### Q33: Number of orders per status
**Natural Language Question:** Number of orders per status

**SQL Query:**
```sql
SELECT 
    "status", 
    COUNT("orderNumber") as "orderCount"
FROM orders
GROUP BY "status"
ORDER BY "orderCount" DESC;
```

**Explanation:**
- Groups orders by their status
- Shows distribution of order statuses
- Useful for order fulfillment tracking

**Expected Result:**
```
Sample output:
status     | orderCount
Shipped    | 303
Resolved   | 14
Cancelled  | 6
On Hold    | 2
Disputed   | 1
In Process | 0
```

---

### Q34: Products per product line
**Natural Language Question:** Products per product line

**SQL Query:**
```sql
SELECT 
    "productLine", 
    COUNT("productCode") as "productCount"
FROM products
GROUP BY "productLine"
ORDER BY "productCount" DESC;
```

**Explanation:**
- Groups products by their category/line
- Shows number of products in each line
- Useful for product portfolio analysis

**Expected Result:**
```
Sample output:
productLine          | productCount
Classic Cars         | 38
Motorcycles          | 13
Planes               | 12
Ships                | 12
Trains               | 3
Trucks and Buses     | 17
Vintage Cars         | 24
```

---

### Q35: Employees per office
**Natural Language Question:** Employees per office

**SQL Query:**
```sql
SELECT 
    o."city", 
    o."country",
    COUNT(e."employeeNumber") as "employeeCount"
FROM employees e
JOIN offices o ON e."officeCode" = o."officeCode"
GROUP BY e."officeCode", o."city", o."country"
ORDER BY "employeeCount" DESC;
```

**Explanation:**
- Groups employees by their office location
- Shows headcount per office
- Useful for organizational structure analysis

**Expected Result:**
```
Sample output:
city          | country | employeeCount
San Francisco | USA     | 6
Boston        | USA     | 3
NYC           | USA     | 2
Paris         | France  | 4
London        | UK      | 2
...
```

---

### Q36: Total stock per product vendor
**Natural Language Question:** Total stock per product vendor

**SQL Query:**
```sql
SELECT 
    "productVendor", 
    SUM("quantityInStock") as "totalStock",
    COUNT("productCode") as "productCount",
    AVG("quantityInStock") as "avgStockPerProduct"
FROM products
GROUP BY "productVendor"
ORDER BY "totalStock" DESC;
```

**Explanation:**
- Groups inventory by supplier/vendor
- SUM shows total items in stock per vendor
- COUNT shows number of products per vendor
- AVG shows average stock level

**Expected Result:**
```
Sample output:
productVendor              | totalStock | productCount | avgStockPerProduct
Min Lin Toys               | 9997       | 13           | 769.00
Classic Metal Creations    | 8324       | 8            | 1040.50
Autoart Studio Design      | 8127       | 14           | 580.50
...
```

---

### Q37: Average buy price per product line
**Natural Language Question:** Average buy price per product line

**SQL Query:**
```sql
SELECT 
    "productLine", 
    AVG("buyPrice") as "avgBuyPrice",
    MIN("buyPrice") as "minBuyPrice",
    MAX("buyPrice") as "maxBuyPrice",
    COUNT("productCode") as "productCount"
FROM products
GROUP BY "productLine"
ORDER BY "avgBuyPrice" DESC;
```

**Explanation:**
- Groups products by line and calculates pricing statistics
- AVG shows average cost per product line
- Useful for cost analysis by category

**Expected Result:**
```
Sample output:
productLine     | avgBuyPrice | minBuyPrice | maxBuyPrice | productCount
Ships           | 58.36       | 29.34       | 82.34       | 12
Planes          | 51.86       | 25.84       | 77.35       | 12
Classic Cars    | 43.26       | 15.26       | 77.32       | 38
...
```

---

### Q38: Orders per customer
**Natural Language Question:** Orders per customer

**SQL Query:**
```sql
SELECT 
    c."customerName", 
    COUNT(o."orderNumber") as "orderCount",
    MAX(o."orderDate") as "lastOrderDate",
    MIN(o."orderDate") as "firstOrderDate"
FROM orders o
JOIN customers c ON o."customerNumber" = c."customerNumber"
GROUP BY o."customerNumber", c."customerName"
ORDER BY "orderCount" DESC;
```

**Explanation:**
- Groups orders by customer
- Shows order frequency and order date range per customer
- Useful for customer activity analysis

**Expected Result:**
```
Sample output:
customerName           | orderCount | lastOrderDate | firstOrderDate
Euro+ Shopping Channel | 26         | 2005-05-26    | 2003-01-31
Mini Gifts Distributors| 17         | 2005-05-16    | 2003-02-14
...
```

---

### Q39: Max MSRP per product line
**Natural Language Question:** Max MSRP per product line

**SQL Query:**
```sql
SELECT 
    "productLine", 
    MAX("MSRP") as "maxMSRP",
    MIN("MSRP") as "minMSRP",
    AVG("MSRP") as "avgMSRP"
FROM products
GROUP BY "productLine"
ORDER BY "maxMSRP" DESC;
```

**Explanation:**
- Groups products by line and shows price ranges
- MAX/MIN show price extremes per category
- Useful for pricing analysis

**Expected Result:**
```
Sample output:
productLine     | maxMSRP | minMSRP | avgMSRP
Ships           | 192.87  | 52.87   | 127.54
Planes          | 207.80  | 48.84   | 108.09
Classic Cars    | 227.80  | 52.26   | 99.33
...
```

---

### Q40: Min buy price per vendor
**Natural Language Question:** Min buy price per vendor

**SQL Query:**
```sql
SELECT 
    "productVendor", 
    MIN("buyPrice") as "minBuyPrice",
    MAX("buyPrice") as "maxBuyPrice",
    AVG("buyPrice") as "avgBuyPrice"
FROM products
GROUP BY "productVendor"
ORDER BY "minBuyPrice" ASC;
```

**Explanation:**
- Shows cost ranges per vendor
- MIN shows cheapest product from each vendor
- Useful for vendor comparison

**Expected Result:**
```
Sample output:
productVendor              | minBuyPrice | maxBuyPrice | avgBuyPrice
Autoart Studio Design      | 15.26       | 77.32       | 48.65
BBC Toy Factory            | 16.34       | 75.25       | 45.78
Classic Metal Creations    | 18.34       | 76.54       | 47.89
...
```

---

### Q41: Total number of customers
**Natural Language Question:** Total number of customers

**SQL Query:**
```sql
SELECT COUNT("customerNumber") as "totalCustomers"
FROM customers;
```

**Explanation:**
- Simple COUNT aggregate without grouping
- Returns single row with total count

**Expected Result:**
```
totalCustomers
122
```

---

### Q42: Total number of products
**Natural Language Question:** Total number of products

**SQL Query:**
```sql
SELECT COUNT("productCode") as "totalProducts"
FROM products;
```

**Explanation:**
- Counts all unique product codes

**Expected Result:**
```
totalProducts
110
```

---

### Q43: Total revenue from payments
**Natural Language Question:** Total revenue from payments

**SQL Query:**
```sql
SELECT SUM("amount") as "totalRevenue"
FROM payments;
```

**Explanation:**
- Sums all payment amounts
- Shows total cash collected

**Expected Result:**
```
totalRevenue
9,646,291.20
```

---

### Q44: Average product price
**Natural Language Question:** Average product price

**SQL Query:**
```sql
SELECT 
    AVG("MSRP") as "avgMSRP",
    AVG("buyPrice") as "avgBuyPrice",
    AVG("MSRP" - "buyPrice") as "avgMargin"
FROM products;
```

**Explanation:**
- Calculates average MSRP (selling price)
- Shows average profit margin

**Expected Result:**
```
avgMSRP      | avgBuyPrice | avgMargin
109.04       | 54.32       | 54.72
```

---

### Q45: Max payment amount
**Natural Language Question:** Max payment amount

**SQL Query:**
```sql
SELECT MAX("amount") as "maxPaymentAmount"
FROM payments;
```

**Explanation:**
- Finds largest single payment

**Expected Result:**
```
maxPaymentAmount
120,166.58
```

---

### Q46: Min payment amount
**Natural Language Question:** Min payment amount

**SQL Query:**
```sql
SELECT MIN("amount") as "minPaymentAmount"
FROM payments;
```

**Explanation:**
- Finds smallest payment amount

**Expected Result:**
```
minPaymentAmount
482.13
```

---

### Q47: Count total orders
**Natural Language Question:** Count total orders

**SQL Query:**
```sql
SELECT COUNT("orderNumber") as "totalOrders"
FROM orders;
```

**Explanation:**
- Counts all order records

**Expected Result:**
```
totalOrders
326
```

---

### Q48: Total quantity in stock
**Natural Language Question:** Total quantity in stock

**SQL Query:**
```sql
SELECT SUM("quantityInStock") as "totalQuantityInStock"
FROM products;
```

**Explanation:**
- Sums inventory across all products

**Expected Result:**
```
totalQuantityInStock
555,926
```

---

### Q49: Average MSRP
**Natural Language Question:** Average MSRP

**SQL Query:**
```sql
SELECT AVG("MSRP") as "averageMSRP"
FROM products;
```

**Explanation:**
- Calculates average retail price
- Same as avg product price

**Expected Result:**
```
averageMSRP
109.04
```

---

### Q50: Number of employees
**Natural Language Question:** Number of employees

**SQL Query:**
```sql
SELECT COUNT("employeeNumber") as "totalEmployees"
FROM employees;
```

**Explanation:**
- Counts all employee records

**Expected Result:**
```
totalEmployees
23
```

---

## Part 2: Evaluation Strategy for Text-to-SQL Agents

### Overview
A Text-to-SQL agent evaluation framework must assess multiple dimensions of system performance, not just query correctness.

### Evaluation Dimensions

#### 1. **SQL Generation Quality**

**Metrics:**
- **Syntactic Correctness**: Does the generated SQL parse without syntax errors?
- **Semantic Correctness**: Does the generated SQL return correct results matching ground truth?
- **Query Efficiency**: Does the query have reasonable complexity? (time complexity, JOIN count)

**Evaluation Method:**
```
For each test question:
- Run generated SQL
- Compare results with ground truth SQL results
- Track execution time
- Record: PASS/FAIL
```

#### 2. **Component Recognition Accuracy**

**Metrics:**
- **Table Selection**: Are correct tables identified? (Precision, Recall)
- **Column Projection**: Are required columns selected?
- **Join Detection**: Are joins correctly identified and executed?
- **Filter Recognition**: Are WHERE conditions properly applied?
- **Aggregation Accuracy**: Are GROUP BY and aggregate functions correct?

**Evaluation Method:**
```
For decomposition task (Task 2):
- Compare extracted tables with ground truth tables
- Compare identified joins with ground truth joins
- Calculate precision/recall for each component
```

#### 3. **Error Handling & Recovery**

**Metrics:**
- **Error Rate**: % of queries with execution errors
- **Retry Success Rate**: % of errors fixed after retry
- **Recovery Latency**: Time to fix and retry
- **Graceful Degradation**: Does system fail gracefully?

**Evaluation Method:**
```
For each failed query:
- Record error message
- Check if retry fixed it
- Track retry count
- Record final status: FIXED/UNFIXED
```

#### 4. **Result Accuracy**

**Metrics:**
- **Exact Match**: Results exactly match ground truth (0% difference)
- **Fuzzy Match**: Results are semantically correct (minor formatting differences)
- **Row Count Accuracy**: Does result have correct number of rows?
- **Value Accuracy**: Are cell values correct?

**Evaluation Method:**
```
For each query result:
- Compare row count with ground truth
- Compare column values
- Check for missing/extra rows
- Assign accuracy score: 0-100%
```

#### 5. **Natural Language Generation Quality**

**Metrics:**
- **Answer Completeness**: Does summary cover all results?
- **Answer Clarity**: Is the summary understandable?
- **Answer Conciseness**: Is it appropriately brief?

**Evaluation Method:**
```
Human review or automated checks:
- Check if summary mentions key statistics
- Check if summary is grammatically correct
- Check readability score
```

#### 6. **System Robustness**

**Metrics:**
- **Ambiguity Handling**: How does system handle ambiguous questions?
- **Complex Query Handling**: Success rate on complex multi-join queries?
- **Null Value Handling**: How well system handles NULL values?

**Evaluation Method:**
```
For edge cases:
- Ambiguous questions (multiple valid interpretations)
- NULL values in filters/joins
- Complex aggregations
- Record success/failure
```

---

### Proposed Evaluation Framework

#### Phase 1: Offline Evaluation (Before Deployment)
```
1. Ground Truth Collection
   - Manually verified SQL for all test questions
   - Expected results for each query
   - Component decomposition (tables, joins, filters)

2. Benchmark Dataset Creation
   - 50 test questions
   - Categorized by difficulty
   - Difficulty categories:
     * Easy: Simple SELECT, no joins
     * Medium: Joins, aggregations
     * Hard: Complex multi-joins, subqueries
     * Edge cases: NULLs, ambiguity

3. Metric Calculation
   - Run agent on all test questions
   - Compare outputs with ground truth
   - Calculate metrics for each query
   - Aggregate into system-level metrics
```

#### Phase 2: Metric Aggregation
```
OVERALL_METRICS = {
    "execution_success_rate": (queries_executed / total_queries) × 100,
    "result_correctness_rate": (correct_results / executed_queries) × 100,
    "retry_success_rate": (fixed_on_retry / failed_queries) × 100,
    "error_handling_score": (graceful_errors / total_errors) × 100,
    "average_latency_ms": avg(query_execution_times),
    "component_accuracy": {
        "table_selection": precision_recall,
        "join_accuracy": precision_recall,
        "filter_accuracy": precision_recall,
        "aggregation_accuracy": precision_recall
    }
}
```

#### Phase 3: Reporting
```
Generate Report:
1. Summary Dashboard
   - Overall success rate
   - Error breakdown
   - Performance metrics

2. Per-Query Analysis
   - Each question with result
   - Accuracy score
   - Error messages (if any)
   - Retry history

3. Category Analysis
   - Easy questions: X% success
   - Medium questions: X% success
   - Hard questions: X% success

4. Failure Analysis
   - Common error types
   - Root causes
   - Recommendations for improvement
```

---

### Evaluation Metrics Matrix

| Metric | Weight | Formula | Threshold |
|--------|--------|---------|-----------|
| SQL Execution Success | 30% | (successful_executions / total_queries) | ≥ 90% |
| Result Correctness | 40% | (correct_results / executed_queries) | ≥ 85% |
| Retry Success Rate | 15% | (fixed_on_retry / initial_failures) | ≥ 70% |
| Response Latency | 10% | avg(execution_time_ms) | ≤ 5000ms |
| Error Handling | 5% | (graceful_failures / total_failures) | ≥ 80% |

**Overall Score = Σ(Metric × Weight)**

---

### Expected Evaluation Output Template

```
TEXT-TO-SQL SYSTEM EVALUATION REPORT
Generated: May 17, 2026

OVERALL PERFORMANCE
- Total Questions: 50
- Successful: 48 (96%)
- Failed: 2 (4%)
- Avg Latency: 245ms

DETAILED RESULTS
┌─────────┬──────────────────────────────┬─────────┬────────────┬──────────┐
│ ID      │ Question                     │ Status  │ Correct    │ Latency  │
├─────────┼──────────────────────────────┼─────────┼────────────┼──────────┤
│ Q1      │ List all products            │ ✓ PASS  │ YES        │ 145ms    │
│ Q21     │ Get orders with customer...  │ ✓ PASS  │ YES        │ 523ms    │
│ Q31     │ Count customers per country  │ ✗ FAIL  │ NO         │ 1200ms   │
│ ...     │ ...                          │ ...     │ ...        │ ...      │
└─────────┴──────────────────────────────┴─────────┴────────────┴──────────┘

BY CATEGORY
- Simple SELECT: 20/20 (100%)
- JOINs: 18/20 (90%)
- Aggregations: 10/10 (100%)

FAILURES
1. Q31: Query generated incorrect GROUP BY clause
2. Q45: Null handling issue in aggregate function

RECOMMENDATIONS
- Improve GROUP BY logic
- Better NULL value handling
```

---

### Implementation in Tasks 3 & 4

The evaluation framework will be integrated as:
- **Task 3**: Generate metrics for each query execution
- **Task 4**: Report metrics in API response

Example Task 4 Output with Metrics:
```json
{
  "question": "Count customers per country",
  "sql": "SELECT country, COUNT(*) FROM customers GROUP BY country",
  "result": [...],
  "metrics": {
    "execution_success": true,
    "result_correctness": 0.95,
    "latency_ms": 234,
    "components_detected": {
      "tables": ["customers"],
      "aggregation": "COUNT",
      "grouping": ["country"]
    }
  },
  "status": "success"
}
```

---

## Summary

This evaluation framework provides a comprehensive approach to assessing Text-to-SQL agent performance across:
1. **SQL Quality** (syntax & semantics)
2. **Component Recognition** (tables, joins, filters)
3. **Error Handling** (recovery, resilience)
4. **Result Accuracy** (correctness, completeness)
5. **NLG Quality** (response clarity)
6. **System Robustness** (edge cases, complexity)

The framework enables iterative improvement of the Text-to-SQL system and provides clear metrics for production readiness.


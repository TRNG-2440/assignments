-- Task 1: Environment Setup 
CREATE OR REPLACE DATABASE tasty_bytes_db;
CREATE OR REPLACE SCHEMA tasty_bytes_db.raw_data;
CREATE OR REPLACE SCHEMA tasty_bytes_db.clean_data;
CREATE OR REPLACE WAREHOUSE TRAINING_WH
WAREHOUSE_SIZE='XSMALL'
AUTO_SUSPEND=300
AUTO_RESUME=True
INITIALLY_SUSPENDED=TRUE;

USE WAREHOUSE TRAINING_WH;

-- Task 4: Create an external stage pointing to the public S3 dataset
CREATE OR REPLACE STAGE tasty_bytes_db.raw_data.menu_stage
URL = 's3://sfquickstarts/tastybytes/raw_pos/menu/';

-- Task 2: Source file exploration 
LIST @tasty_bytes_db.raw_data.menu_stage;

SELECT $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11
FROM @tasty_bytes_db.raw_data.menu_stage
LIMIT 10;

-- Task 3: Create a file format for the menu file 
CREATE OR REPLACE FILE FORMAT tasty_bytes_db.raw_data.tasty_bytes_csv_format
  TYPE = 'CSV'
  FIELD_DELIMITER = ','
  SKIP_HEADER = 1
  EMPTY_FIELD_AS_NULL = TRUE;
  
SELECT $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11
FROM @tasty_bytes_db.raw_data.menu_stage/menu.csv.gz
(FILE_FORMAT => tasty_bytes_db.raw_data.tasty_bytes_csv_format);

-- Task 5: Raw data loading
CREATE OR REPLACE TABLE tasty_bytes_db.raw_data.menu (
    menu_id NUMBER(19,0),
    truck_brand_name VARCHAR(16777216),
    menu_item_name VARCHAR(16777216),
    item_category VARCHAR(16777216),
    item_subcategory VARCHAR(16777216),
    cost_price NUMBER(38,4),
    sale_price NUMBER(38,4)
);

INSERT INTO tasty_bytes_db.raw_data.menu (menu_id, truck_brand_name, menu_item_name, item_category, item_subcategory, cost_price, sale_price)
SELECT $1, $4, $6, $7, $8, $9, $10
FROM @tasty_bytes_db.raw_data.menu_stage/menu.csv.gz
(FILE_FORMAT => tasty_bytes_db.raw_data.tasty_bytes_csv_format);

SELECT * FROM tasty_bytes_db.raw_data.menu;

-- Task 6: Data validation
-- 1. Find total number of menu items
-- Ans: 99
SELECT COUNT(menu_item_name) AS menu_item_count
FROM tasty_bytes_db.raw_data.menu;

-- 2. Number of unique truck brands
-- Ans: 15
SELECT COUNT(DISTINCT truck_brand_name) AS uniq_truck_brand_count
FROM tasty_bytes_db.raw_data.menu;

-- 3. Number of unique categories
-- Ans: 4
SELECT COUNT(DISTINCT item_category) AS uniq_item_category_count
FROM tasty_bytes_db.raw_data.menu;

-- 4. Minimum sale price
-- Ans: 2.0000
SELECT MIN(sale_price) AS min_sale_price
FROM tasty_bytes_db.raw_data.menu;

-- 5. Maximum sale price
-- Ans: 21.0000
SELECT MAX(sale_price) AS max_sale_price
FROM tasty_bytes_db.raw_data.menu;

-- 6. Average sale price
-- Ans: 7.2146
SELECT ROUND(AVG(sale_price), 4) AS avg_sale_price
FROM tasty_bytes_db.raw_data.menu;

-- Task 7: Transform the data
CREATE OR REPLACE TABLE tasty_bytes_db.clean_data.menu 
AS SELECT 
    menu_id, 
    UPPER(TRIM(truck_brand_name)) AS truck_brand_name,
    TRIM(menu_item_name) AS menu_item_name,
    UPPER(TRIM(item_category)) AS item_category,
    item_subcategory,
    cost_price,
    sale_price, 
    sale_price - cost_price AS profit,
    ROUND(((sale_price - cost_price)/ cost_price) * 100, 4) AS profit_percentage,
    CASE 
        WHEN sale_price < 5 THEN 'BUDGET'
        WHEN sale_price BETWEEN 5 AND 10 THEN 'STANDARD'
        WHEN sale_price BETWEEN 10 AND 15 THEN 'PREMIUM'
        ELSE 'LUXURY' END
     AS price_category,
    CONCAT_WS('-', truck_brand_name, menu_item_name) AS display_name,
    CURRENT_TIMESTAMP() AS load_timestamp
FROM tasty_bytes_db.raw_data.menu;

SELECT * FROM tasty_bytes_db.clean_data.menu;

-- Task 8: Business Analysis
-- 1. What are the 5 most expensive menu items
SELECT  
    truck_brand_name,
    menu_item_name,
    sale_price
FROM tasty_bytes_db.clean_data.menu
ORDER BY sale_price DESC 
LIMIT 5;

-- 2. What are the 5 most profitable menu items
SELECT
    truck_brand_name, 
    menu_item_name,
    profit_percentage,
FROM tasty_bytes_db.clean_data.menu
ORDER BY profit_percentage DESC 
LIMIT 5;

-- 3. Which truck brand has the highest average selling price?
SELECT 
    truck_brand_name,
    AVG(sale_price) as avg_sale_price
FROM tasty_bytes_db.clean_data.menu
GROUP BY truck_brand_name
ORDER BY avg_sale_price DESC
LIMIT 1;

-- 4. Which truck brand has the highest average profit? 
SELECT 
    truck_brand_name,
    AVG(profit) AS avg_profit,
    AVG(profit_percentage) AS avg_profit_percentage
FROM tasty_bytes_db.clean_data.menu 
GROUP BY truck_brand_name
ORDER BY avg_profit DESC
LIMIT 1;

-- 5. How many menu items belong to each category?
SELECT item_category, COUNT(menu_item_name) as menu_item_count
FROM tasty_bytes_db.clean_data.menu 
GROUP BY item_category;

-- 6. How many menu items belong to each price category?
SELECT price_category, COUNT(menu_item_name) aS menu_item_count
FROM tasty_bytes_db.clean_data.menu
GROUP BY price_category;

-- Task 9: Data quality
-- 1. Find the number of records with:
--      1. Missing menu item name
--      2. Missing category
--      3. Missing cost price
--      4. Missing sale price
SELECT 
    COUNT(*) - COUNT(menu_item_name) AS missing_menu_item_name,
    COUNT(*) - COUNT(item_category) AS missing_categories,
    COUNT(*) - COUNT(cost_price) AS missing_cost_price,
    COUNT(*) - COUNT(sale_price) AS missing_sale_price
FROM tasty_bytes_db.clean_data.menu;

-- 2. Create a simple quality status:
-- All important values available -> GOOD
-- One value missing -> REVIEW
-- Multiple values misisng -> POOR
-- 2. Create a simple quality status:
-- All important values available -> GOOD
-- One value missing -> REVIEW
-- Multiple values missing -> POOR
SELECT 
    menu_id,
    menu_item_name,
    item_category,
    cost_price,
    sale_price,
    CASE 
        WHEN (CASE WHEN menu_item_name IS NULL THEN 1 ELSE 0 END +
              CASE WHEN item_category IS NULL THEN 1 ELSE 0 END +
              CASE WHEN cost_price IS NULL THEN 1 ELSE 0 END +
              CASE WHEN sale_price IS NULL THEN 1 ELSE 0 END) = 0 THEN 'GOOD'
        WHEN (CASE WHEN menu_item_name IS NULL THEN 1 ELSE 0 END +
              CASE WHEN item_category IS NULL THEN 1 ELSE 0 END +
              CASE WHEN cost_price IS NULL THEN 1 ELSE 0 END +
              CASE WHEN sale_price IS NULL THEN 1 ELSE 0 END) = 1 THEN 'REVIEW'
        ELSE 'POOR'
    END AS quality_status
FROM tasty_bytes_db.clean_data.menu;

-- Task 10: Create a brand level summary containing:
-- Truck brand name
-- Total menu items
-- Average sale price
-- Average profit
-- Maximum sale price
-- Minimum sale price

SELECT 
    truck_brand_name,
    COUNT(menu_item_name) AS total_menu_items,
    ROUND(AVG(sale_price), 2) AS avg_sale_price,
    ROUND(AVG(profit), 2) AS avg_profit,
    MAX(sale_price) AS max_sale_price,
    MIN(sale_price) AS min_sale_price
FROM tasty_bytes_db.clean_data.menu
GROUP BY truck_brand_name
ORDER BY avg_profit DESC;
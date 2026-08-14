-- Task 1: Setup environment

CREATE DATABASE IF NOT EXISTS Food_Truck_DB;

CREATE SCHEMA IF NOT EXISTS Food_Truck_DB.RAW;

CREATE SCHEMA IF NOT EXISTS Food_Truck_DB.CLEAN;

CREATE WAREHOUSE IF NOT EXISTS Food_Truck_WH
  WAREHOUSE_SIZE = 'XSMALL'
  AUTO_SUSPEND = 60
  AUTO_RESUME = TRUE
  INITIALLY_SUSPENDED = TRUE;

USE WAREHOUSE TASTYBYTES_WH;
USE DATABASE TASTYBYTES_DB;
USE SCHEMA RAW;

----------------------------------------------------------------------

-- Task 2: Source file exploration
CREATE OR REPLACE STAGE Food_Truck_DB.RAW.MENU_EXPLORE_STAGE
 URL = 's3://sfquickstarts/tastybytes/raw_pos/menu/';

LIST @Food_Truck_DB.RAW.MENU_EXPLORE_STAGE;

SELECT
  METADATA$FILENAME AS file_name,
  $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11
FROM @Food_Truck_DB.RAW.MENU_EXPLORE_STAGE
LIMIT 5;


-- Task 3: File Format
CREATE OR REPLACE FILE FORMAT Food_Truck_DB.RAW.MENU_CSV_FF
  TYPE = CSV
  FIELD_DELIMITER = ','
  SKIP_HEADER = 1
  FIELD_OPTIONALLY_ENCLOSED_BY = '"'
  NULL_IF = ('NULL', 'null', '')
  COMPRESSION = GZIP;

----------------------------------------------------------------------

-- Task 3: File Format
CREATE OR REPLACE FILE FORMAT Food_Truck_DB.RAW.MENU_CSV_FF
  TYPE = CSV
  FIELD_DELIMITER = ','
  SKIP_HEADER = 1
  FIELD_OPTIONALLY_ENCLOSED_BY = '"'
  NULL_IF = ('NULL', 'null', '')
  COMPRESSION = GZIP;

----------------------------------------------------------------------

-- 4) External Stage
CREATE OR REPLACE STAGE Food_Truck_DB.RAW.MENU_STAGE
  URL = 's3://sfquickstarts/tastybytes/raw_pos/menu/'
  FILE_FORMAT = Food_Truck_DB.RAW.MENU_CSV_FF;

-- Verify
LIST @Food_Truck_DB.RAW.MENU_STAGE;

----------------------------------------------------------------------


-- 5) Raw data loading
CREATE OR REPLACE TABLE Food_Truck_DB.RAW.MENU_RAW (
  MENU_ID NUMBER(19,0),
  MENU_TYPE_ID NUMBER(38,0),
  MENU_TYPE VARCHAR,
  TRUCK_BRAND_NAME VARCHAR,
  MENU_ITEM_ID NUMBER(38,0),
  MENU_ITEM_NAME VARCHAR,
  ITEM_CATEGORY VARCHAR,
  ITEM_SUBCATEGORY VARCHAR,
  COST_PRICE NUMBER(38,4),
  SALE_PRICE NUMBER(38,4),
  MENU_ITEM_HEALTH_METRICS_OBJ VARIANT
);

-- Import from stage
COPY INTO Food_Truck_DB.RAW.MENU_RAW
FROM @Food_Truck_DB.RAW.MENU_STAGE;

-- Check the data
SELECT * FROM Food_Truck_DB.RAW.MENU_RAW LIMIT 10;

----------------------------------------------------------------------

-- Task 6: Data Validation
SELECT
  COUNT(*) AS total_menu_items,
  COUNT(DISTINCT TRUCK_BRAND_NAME) AS unique_truck_brands,
  COUNT(DISTINCT ITEM_CATEGORY) AS unique_categories,
  MIN(SALE_PRICE) AS min_sale_price,
  MAX(SALE_PRICE) AS max_sale_price,
  ROUND(AVG(SALE_PRICE), 2) AS avg_sale_price
FROM Food_Truck_DB.RAW.MENU_RAW;

----------------------------------------------------------------------

-- Task 7: Transform the Data 
-- 1) Clean menu table and remove unnecessary spaces
CREATE OR REPLACE TABLE Food_Truck_DB.CLEAN.MENU_CLEAN AS
SELECT
  MENU_ID,
  MENU_ITEM_ID,


  TRIM(MENU_ITEM_NAME) AS MENU_ITEM_NAME,

  -- 2) Standardize Brand Name
  UPPER(TRUCK_BRAND_NAME) AS TRUCK_BRAND_NAME,

  -- 3) Standardize Category
  UPPER(ITEM_CATEGORY) AS ITEM_CATEGORY,

  ITEM_SUBCATEGORY,
  COST_PRICE,
  SALE_PRICE,

  -- 4) Calculate Profit
  (SALE_PRICE - COST_PRICE) AS PROFIT,

  -- 5) Calculate Profit Percentage
  ROUND(((SALE_PRICE - COST_PRICE) / NULLIF(SALE_PRICE, 0)) * 100, 2)
    AS PROFIT_PERCENTAGE,

  -- 6) Create Price Category
  CASE
    WHEN SALE_PRICE < 5 THEN 'BUDGET'              -- Below 5
    WHEN SALE_PRICE >= 5 AND SALE_PRICE < 10 THEN 'STANDARD'   -- 5 to below 10
    WHEN SALE_PRICE >= 10 AND SALE_PRICE < 15 THEN 'PREMIUM'   -- 10 to below 15
    WHEN SALE_PRICE >= 15 THEN 'LUXURY'            -- 15 and above
  END AS PRICE_CATEGORY,

  -- 7) Create Display Name 
  UPPER(TRUCK_BRAND_NAME) || ' - ' || TRIM(MENU_ITEM_NAME) AS DISPLAY_NAME,

  -- 8) Add Load Timestamp
  CURRENT_TIMESTAMP() AS LOAD_TIMESTAMP

FROM Food_Truck_DB.RAW.MENU_RAW;

----------------------------------------------------------------------

-- 1) What are the 5 most expensive menu items?
SELECT
  DISPLAY_NAME,
  MENU_ITEM_NAME,
  TRUCK_BRAND_NAME,
  SALE_PRICE
FROM Food_Truck_DB.CLEAN.MENU_CLEAN
ORDER BY SALE_PRICE DESC
LIMIT 5

-- 2) 5 most profitable menu items
SELECT
  DISPLAY_NAME,
  MENU_ITEM_NAME,
  TRUCK_BRAND_NAME,
  PROFIT,
  SALE_PRICE,
  COST_PRICE
FROM Food_Truck_DB.CLEAN.MENU_CLEAN
ORDER BY PROFIT DESC
LIMIT 5;

-- 3) Which truck brand has the highest average selling price
SELECT
  TRUCK_BRAND_NAME,
  ROUND(AVG(SALE_PRICE), 2) AS average_sale_price
FROM Food_Truck_DB.CLEAN.MENU_CLEAN
GROUP BY TRUCK_BRAND_NAME
ORDER BY average_sale_price DESC
LIMIT 1;

-- 4) Which truck brand has the highest average profit
SELECT
  TRUCK_BRAND_NAME,
  ROUND(AVG(PROFIT), 2) AS avg_profit
FROM Food_Truck_DB.CLEAN.MENU_CLEAN
GROUP BY TRUCK_BRAND_NAME
ORDER BY avg_profit DESC
LIMIT 1;

-- 5) How many menu items belong to each category?
SELECT
  ITEM_CATEGORY,
  COUNT(*) AS item_count
FROM Food_Truck_DB.CLEAN.MENU_CLEAN
GROUP BY ITEM_CATEGORY
ORDER BY item_count DESC;

-- 6) How many items belong to each Price Category?
SELECT
  PRICE_CATEGORY,
  COUNT(*) AS item_count
FROM Food_Truck_DB.CLEAN.MENU_CLEAN
GROUP BY PRICE_CATEGORY
ORDER BY item_count DESC;

----------------------------------------------------------------------

-- 9) Data Quality

-- 1. Find the following records: missing menu item name, missing category, missing cost price and missing sales price
SELECT
  SUM(CASE WHEN MENU_ITEM_NAME IS NULL OR MENU_ITEM_NAME = '' THEN 1 ELSE 0 END) AS missing_name,
  SUM(CASE WHEN ITEM_CATEGORY IS NULL OR ITEM_CATEGORY = '' THEN 1 ELSE 0 END) AS missing_category,
  SUM(CASE WHEN COST_PRICE IS NULL THEN 1 ELSE 0 END) AS missing_cost,
  SUM(CASE WHEN SALE_PRICE IS NULL THEN 1 ELSE 0 END) AS missing_sale
FROM Food_Truck_DB.CLEAN.MENU_CLEAN;

-- 2. Find the following records: Important values available, one value missing, multiple values missing
SELECT
  MENU_ID,
  MENU_ITEM_NAME,
  ITEM_CATEGORY,
  COST_PRICE,
  SALE_PRICE,
  CASE
    WHEN MENU_ITEM_NAME IS NOT NULL
     AND MENU_ITEM_NAME <> ''
     AND ITEM_CATEGORY IS NOT NULL
     AND ITEM_CATEGORY <> ''
     AND COST_PRICE IS NOT NULL
     AND SALE_PRICE IS NOT NULL
    THEN 'GOOD'
    WHEN (CASE WHEN MENU_ITEM_NAME IS NULL OR MENU_ITEM_NAME = '' THEN 1 ELSE 0 END)
       + (CASE WHEN ITEM_CATEGORY IS NULL OR ITEM_CATEGORY = '' THEN 1 ELSE 0 END)
       + (CASE WHEN COST_PRICE IS NULL THEN 1 ELSE 0 END)
       + (CASE WHEN SALE_PRICE IS NULL THEN 1 ELSE 0 END) = 1
    THEN 'REVIEW'
    ELSE 'POOR'
  END AS QUALITY_STATUS
FROM Food_Truck_DB.CLEAN.MENU_CLEAN;

----------------------------------------------------------------------

-- Task 10: Truck brand summary- Truck brand name, average sales price, average profit, minimum sales price and maximum sales price
SELECT
  TRUCK_BRAND_NAME,
  COUNT(*) AS total_menu_items,
  ROUND(AVG(SALE_PRICE), 2) AS average_sale_price,
  ROUND(AVG(PROFIT), 2) AS average_profit,
  MIN(SALE_PRICE) AS minimum_sale_price,
  MAX(SALE_PRICE) AS maximum_sale_price
FROM Food_Truck_DB.CLEAN.MENU_CLEAN
GROUP BY TRUCK_BRAND_NAME
ORDER BY average_profit DESC;


-- Most profitable truck brand
SELECT
  TRUCK_BRAND_NAME AS most_profitable_brand,
  ROUND(AVG(PROFIT), 2) AS average_profit
FROM Food_Truck_DB.CLEAN.MENU_CLEAN
GROUP BY TRUCK_BRAND_NAME
ORDER BY average_profit DESC
LIMIT 1;



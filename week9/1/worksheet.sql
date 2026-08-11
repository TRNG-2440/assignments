CREATE OR REPLACE DATABASE Week9;

CREATE OR REPLACE TRANSIENT SCHEMA Week9.raw_schema;

CREATE OR REPLACE SCHEMA Week9.clean_schema;

CREATE OR REPLACE WAREHOUSE Week9Warehouse
WITH
WAREHOUSE_SIZE = XSMALL;

USE DATABASE Week9;
USE SCHEMA raw_schema;
USE WAREHOUSE Week9Warehouse;


--1. Why is a warehouse required?
-- A warehouse is required to actually have the compute
--2. Why do we separate raw and clean data
--Raw data is the unprocessed, we want it for auditability of the clean data, in case the clean data has an incorrect transformation. The clean data is used for the analysis.

--SET source_folder = 'S3://sfquickstarts/tastybytes/raw_pos/menu/';


--Questions
--1. What file type did you configure?
--CSV
--2. What delimiter did you use?
-- comma
--3. How did you handle the header?
-- there is no header
--4. Why is a File Format required?
-- to define how the file actually looks like
--Questions
--1. What is the purpose of a Stage?
-- it is the link between the storage and the database, giving metadata and other things to help with loading
--2. Does the Stage actually store the data inside Snowflake?
-- no, it is a bridge


CREATE OR REPLACE FILE FORMAT menu_file_format
    TYPE = 'CSV'
    FIELD_DELIMITER = ','
    SKIP_HEADER = 0;

CREATE OR REPLACE STAGE menu_stage
    URL = 's3://sfquickstarts/tastybytes/raw_pos/menu/'
    FILE_FORMAT = menu_file_format;

LIST @menu_stage;

CREATE OR REPLACE TABLE raw_menu (
    RECORD_ID         INT,
    MENU_ID         INT,
    TRUCK_TYPE      VARCHAR,
    TRUCK_BRAND     VARCHAR,
    ITEM_ID         INT,
    ITEM_NAME       VARCHAR,
    ITEM_CATEGORY   VARCHAR,
    ITEM_OPTION     VARCHAR,
    COST_PRICE      NUMBER(20,4),
    SALE_PRICE      NUMBER(20,4),
    MENU_METRICS    VARIANT
);

SELECT $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11 FROM @menu_stage/menu.csv.gz;

TRUNCATE raw_menu;

COPY INTO raw_menu FROM @menu_stage/menu.csv.gz
VALIDATION_MODE = 'RETURN_ERRORS';
-- 0 errors

COPY INTO raw_menu FROM @menu_stage;

--file	status	rows_parsed	rows_loaded	error_limit	errors_seen	first_error	first_error_line	first_error_character	first_error_column_name
--s3://sfquickstarts/tastybytes/raw_pos/menu/menu.csv.gz	LOADED	100	100	1	0

--data validation

SELECT Count(*) as total_menu_items,
COUNT(DISTINCT TRUCK_BRAND) as unique_truck_brands,
COUNT(DISTINCT ITEM_CATEGORY) as unique_categories,
MIN(sale_price) as min_sale_price,
MAX(sale_price) as max_sale_price,
AVG(sale_price) as avg_sale_price
FROM raw_menu;

--TOTAL_MENU_ITEMS	UNIQUE_TRUCK_BRANDS	UNIQUE_CATEGORIES	MIN_SALE_PRICE	MAX_SALE_PRICE	AVG_SALE_PRICE
--100	15	4	2	21	7.190000

USE SCHEMA clean_schema;


CREATE OR REPLACE TABLE clean_menu (
    RECORD_ID       INT,
    MENU_ID         INT,
    DISPLAY_NAME VARCHAR,
    TRUCK_TYPE      VARCHAR,
    TRUCK_BRAND     VARCHAR,
    ITEM_ID         INT,
    ITEM_NAME       VARCHAR,
    ITEM_CATEGORY   VARCHAR,
    ITEM_OPTION     VARCHAR,
    COST_PRICE      NUMBER(20,4),
    SALE_PRICE      NUMBER(20,4),
    PROFIT          NUMBER(20,4),
    PROFIT_PERCENT  NUMBER(20,4),
    PRICE_CATEGORY   VARCHAR,
    MENU_METRICS    VARIANT,
    LOAD_TIME       TIMESTAMP
);
CREATE OR REPLACE FUNCTION STANDARDIZE_NAME(NAME_VALUE VARCHAR)
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
    TRIM(UPPER(NAME_VALUE))
$$;

CREATE OR REPLACE FUNCTION PRICE_CATEGORY_FN(PRICE NUMBER(20, 4))
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
    CASE
        WHEN PRICE < 5 THEN 'BUDGET'
        WHEN PRICE < 10 THEN 'STANDARD'
        WHEN PRICE < 15 THEN 'PREMIUM'
        ELSE 'LUXURY'
    END
$$;

INSERT INTO clean_menu (RECORD_ID, MENU_ID, DISPLAY_NAME, TRUCK_TYPE, TRUCK_BRAND, ITEM_ID, ITEM_NAME, ITEM_CATEGORY, ITEM_OPTION, COST_PRICE, SALE_PRICE, PROFIT, PROFIT_PERCENT, PRICE_CATEGORY, MENU_METRICS, LOAD_TIME)
SELECT
    RECORD_ID,
    MENU_ID,
    STANDARDIZE_NAME(TRUCK_BRAND) || ' - ' || TRIM(ITEM_NAME) AS DISPLAY_NAME,
    STANDARDIZE_NAME(TRUCK_TYPE) AS TRUCK_TYPE,
    STANDARDIZE_NAME(TRUCK_BRAND) AS TRUCK_BRAND,
    ITEM_ID,
    TRIM(ITEM_NAME) AS ITEM_NAME,
    STANDARDIZE_NAME(ITEM_CATEGORY) AS ITEM_CATEGORY,
    STANDARDIZE_NAME(ITEM_OPTION) AS ITEM_OPTION,
    COST_PRICE,
    SALE_PRICE,
    SALE_PRICE-COST_PRICE AS PROFIT,
    (SALE_PRICE-COST_PRICE)/SALE_PRICE AS PROFIT_PERCENT,
    PRICE_CATEGORY_FN(SALE_PRICE) AS PRICE_CATEGORY,
    MENU_METRICS,
    CURRENT_TIMESTAMP()
FROM raw_schema.raw_menu;


SELECT * FROM clean_menu LIMIT 5;

--5 most expensive items
SELECT ITEM_ID, ITEM_NAME, SALE_PRICE FROM clean_menu
ORDER BY SALE_PRICE DESC
LIMIT 5;

--ITEM_ID	ITEM_NAME	SALE_PRICE
--28	Rack of Pork Ribs	21.0000
--121	The King Combo	20.0000
--142	Tandoori Mixed Grill	18.0000
--53	Tonkotsu Ramen	17.0000
--51	Creamy Chicken Ramen	17.0000

--5 most profitable items
SELECT ITEM_ID, ITEM_NAME, PROFIT FROM clean_menu
ORDER BY PROFIT DESC
LIMIT 5;

--ITEM_ID	ITEM_NAME	PROFIT
--28	Rack of Pork Ribs	10.0000
--52	Spicy Miso Vegetable Ramen	10.0000
--37	Chicken Burrito	10.0000
--53	Tonkotsu Ramen	10.0000
--51	Creamy Chicken Ramen	9.0000

-- truck brand highest average selling price

SELECT TRUCK_BRAND, AVG(SALE_PRICE) FROM clean_menu
GROUP BY TRUCK_BRAND
ORDER BY AVG(SALE_PRICE) DESC
LIMIT 1;

--KITAKATA RAMEN BAR	9.8333333333

--highest average profit
SELECT TRUCK_BRAND, AVG(PROFIT) FROM clean_menu
GROUP BY TRUCK_BRAND
ORDER BY AVG(PROFIT) DESC
LIMIT 1;

--KITAKATA RAMEN BAR	5.6666666667

--how many items per category
SELECT ITEM_CATEGORY, COUNT(*) FROM clean_menu
GROUP BY ITEM_CATEGORY;

--ITEM_CATEGORY	COUNT(*)
--MAIN	43
--SNACK	5
--BEVERAGE	46
--DESSERT	6

--how many items to price category
SELECT PRICE_CATEGORY, COUNT(*) FROM clean_menu
GROUP BY PRICE_CATEGORY;

--PRICE_CATEGORY	COUNT(*)
--BUDGET	48
--PREMIUM	23
--STANDARD	18
--LUXURY	11

SELECT
      COUNT(*) AS total_records,
      COUNT_IF(ITEM_NAME     IS NULL) AS missing_item_name,
      COUNT_IF(ITEM_CATEGORY IS NULL) AS missing_category,
      COUNT_IF(COST_PRICE    IS NULL) AS missing_cost_price,
      COUNT_IF(SALE_PRICE    IS NULL) AS missing_sale_price
  FROM clean_menu;

--TOTAL_RECORDS	MISSING_ITEM_NAME	MISSING_CATEGORY	MISSING_COST_PRICE	MISSING_SALE_PRICE
--100	0	0	0	0

-- no missing records


SELECT TRUCK_BRAND, COUNT(*) AS total_menu_items, AVG(SALE_PRICE) AS average_sale_price, AVG(PROFIT) AS average_profit, MIN(SALE_PRICE) AS min_sale_price, MAX(SALE_PRICE) as max_sale_price FROM clean_menu
GROUP BY TRUCK_BRAND
ORDER BY AVG(PROFIT) DESC;


--TRUCK_BRAND	TOTAL_MENU_ITEMS	AVERAGE_SALE_PRICE	AVERAGE_PROFIT	MIN_SALE_PRICE	MAX_SALE_PRICE
--KITAKATA RAMEN BAR	6	9.8333333333	5.6666666667	2.0000	17.0000
--GUAC N' ROLL	9	8.5555555556	4.8888888889	2.0000	13.0000
--REVENGE OF THE CURDS	6	7.6666666667	4.6666666667	2.0000	14.0000
--SMOKY BBQ	9	9.3333333333	4.5555555556	2.0000	21.0000
--LE COIN DES CRÊPES	6	7.3333333333	4.3333333333	2.0000	15.0000
--NANI'S KITCHEN	6	9.6666666667	4.1666666667	2.0000	18.0000
--CHEEKY GREEK	6	8.5000000000	4.0000000000	2.0000	20.0000
--TASTY TIBS	6	6.8333333333	3.8333333333	2.0000	13.0000
--PEKING TRUCK	6	6.3333333333	3.6666666667	2.0000	13.0000
--THE MAC SHACK	6	6.8333333333	3.1666666667	2.0000	15.0000
--AMPED UP FRANKS	6	5.8333333333	3.1666666667	2.0000	10.0000
--PLANT PALACE	6	6.0000000000	3.0000000000	2.0000	12.0000
--BETTER OFF BREAD	6	6.8333333333	2.8333333333	2.0000	11.0000
--FREEZING POINT	10	4.3000000000	2.7000000000	2.0000	7.0000
--THE MEGA MELT	6	4.1666666667	2.5000000000	2.0000	6.0000
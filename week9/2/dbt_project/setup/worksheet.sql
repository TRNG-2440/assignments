CREATE WAREHOUSE IF NOT EXISTS DBT_BRAZIL_WH
    WAREHOUSE_SIZE = XSMALL
    AUTO_SUSPEND = 60
    AUTO_RESUME = TRUE;

CREATE DATABASE IF NOT EXISTS DBT_BRAZIL;
CREATE SCHEMA IF NOT EXISTS DBT_BRAZIL.OLIST_RAW;

USE WAREHOUSE DBT_BRAZIL_WH;
USE SCHEMA DBT_BRAZIL.OLIST_RAW;

CREATE OR REPLACE FILE FORMAT OLIST_CSV
    TYPE = CSV
    FIELD_DELIMITER = ','
    SKIP_HEADER = 1
    EMPTY_FIELD_AS_NULL = TRUE;

CREATE OR REPLACE TABLE CUSTOMERS (
    CUSTOMER_ID                 STRING,
    CUSTOMER_UNIQUE_ID          STRING,
    CUSTOMER_ZIP_CODE_PREFIX    STRING,
    CUSTOMER_CITY               STRING,
    CUSTOMER_STATE              STRING
);

CREATE OR REPLACE TABLE ORDERS (
    ORDER_ID                        STRING,
    CUSTOMER_ID                     STRING,
    ORDER_STATUS                    STRING,
    ORDER_PURCHASE_TIMESTAMP        TIMESTAMP_NTZ,
    ORDER_APPROVED_AT               TIMESTAMP_NTZ,
    ORDER_DELIVERED_CARRIER_DATE    TIMESTAMP_NTZ,
    ORDER_DELIVERED_CUSTOMER_DATE   TIMESTAMP_NTZ,
    ORDER_ESTIMATED_DELIVERY_DATE   TIMESTAMP_NTZ
);

CREATE OR REPLACE TABLE ORDER_ITEMS (
    ORDER_ID            STRING,
    ORDER_ITEM_ID       NUMBER,
    PRODUCT_ID          STRING,
    SELLER_ID           STRING,
    SHIPPING_LIMIT_DATE TIMESTAMP_NTZ,
    PRICE               NUMBER(12,2),
    FREIGHT_VALUE       NUMBER(12,2)
);

CREATE OR REPLACE TABLE PRODUCTS (
    PRODUCT_ID                  STRING,
    PRODUCT_CATEGORY_NAME       STRING,
    PRODUCT_NAME_LENGHT         NUMBER,
    PRODUCT_DESCRIPTION_LENGHT  NUMBER,
    PRODUCT_PHOTOS_QTY          NUMBER,
    PRODUCT_WEIGHT_G            NUMBER,
    PRODUCT_LENGTH_CM           NUMBER,
    PRODUCT_HEIGHT_CM           NUMBER,
    PRODUCT_WIDTH_CM            NUMBER
);

CREATE OR REPLACE TABLE ORDER_PAYMENTS (
    ORDER_ID                STRING,
    PAYMENT_SEQUENTIAL      NUMBER,
    PAYMENT_TYPE            STRING,
    PAYMENT_INSTALLMENTS    NUMBER,
    PAYMENT_VALUE           NUMBER(12,2)
);

CREATE OR REPLACE TABLE PRODUCT_CATEGORY_TRANSLATION (
    PRODUCT_CATEGORY_NAME           STRING,
    PRODUCT_CATEGORY_NAME_ENGLISH   STRING
);

USE WAREHOUSE DBT_BRAZIL_WH;
USE SCHEMA DBT_BRAZIL.OLIST_RAW;

-- Allow egress to the one host we need, and nothing else
CREATE OR REPLACE NETWORK RULE OLIST_GITHUB_RULE
    MODE = EGRESS
    TYPE = HOST_PORT
    VALUE_LIST = ('raw.githubusercontent.com');

CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION OLIST_GITHUB_INTEGRATION
    ALLOWED_NETWORK_RULES = (OLIST_GITHUB_RULE)
    ENABLED = TRUE;

-- Internal stage the CSVs land in
CREATE OR REPLACE STAGE OLIST_STAGE
    FILE_FORMAT = OLIST_CSV;

-- Download each file and write it to the stage
CREATE OR REPLACE PROCEDURE LOAD_OLIST_FILES()
RETURNS STRING
LANGUAGE PYTHON
RUNTIME_VERSION = '3.11'
PACKAGES = ('snowflake-snowpark-python', 'requests')
HANDLER = 'main'
EXTERNAL_ACCESS_INTEGRATIONS = (OLIST_GITHUB_INTEGRATION)
AS
$$
import io
import requests

BASE = ('https://raw.githubusercontent.com/Ganesh7699/'
        'Brazilian-E-Commerce-OList/master/')

FILES = [
    'olist_customers_dataset.csv',
    'olist_orders_dataset.csv',
    'olist_order_items_dataset.csv',
    'olist_products_dataset.csv',
    'olist_order_payments_dataset.csv',
    'product_category_name_translation.csv',
]

STAGE = '@DBT_BRAZIL.OLIST_RAW.OLIST_STAGE'

def main(session):
    report = []
    for name in FILES:
        response = requests.get(BASE + name, timeout=180)
        response.raise_for_status()
        session.file.put_stream(
            io.BytesIO(response.content),
            f'{STAGE}/{name}',
            auto_compress=False,
            overwrite=True,
        )
        report.append(f'{name}: {len(response.content):,} bytes')
    return '\n'.join(report)
$$;

CALL LOAD_OLIST_FILES();

-- Confirm six files are staged
LIST @OLIST_STAGE;


-- Load each staged file into its table.
-- COPY INTO parses the CSV properly, including quoted fields containing commas.
COPY INTO DBT_BRAZIL.OLIST_RAW.CUSTOMERS
    FROM @OLIST_STAGE/olist_customers_dataset.csv
    FILE_FORMAT = (FORMAT_NAME = OLIST_CSV);

COPY INTO DBT_BRAZIL.OLIST_RAW.ORDERS
    FROM @OLIST_STAGE/olist_orders_dataset.csv
    FILE_FORMAT = (FORMAT_NAME = OLIST_CSV);

COPY INTO DBT_BRAZIL.OLIST_RAW.ORDER_ITEMS
    FROM @OLIST_STAGE/olist_order_items_dataset.csv
    FILE_FORMAT = (FORMAT_NAME = OLIST_CSV);

COPY INTO DBT_BRAZIL.OLIST_RAW.PRODUCTS
    FROM @OLIST_STAGE/olist_products_dataset.csv
    FILE_FORMAT = (FORMAT_NAME = OLIST_CSV);

COPY INTO DBT_BRAZIL.OLIST_RAW.ORDER_PAYMENTS
    FROM @OLIST_STAGE/olist_order_payments_dataset.csv
    FILE_FORMAT = (FORMAT_NAME = OLIST_CSV);

COPY INTO DBT_BRAZIL.OLIST_RAW.PRODUCT_CATEGORY_TRANSLATION
    FROM @OLIST_STAGE/product_category_name_translation.csv
    FILE_FORMAT = (FORMAT_NAME = OLIST_CSV);


-- Verify: every ROW_COUNT must equal its EXPECTED
SELECT 'CUSTOMERS' AS TABLE_NAME, COUNT(*) AS ROW_COUNT, 99441 AS EXPECTED
FROM DBT_BRAZIL.OLIST_RAW.CUSTOMERS
UNION ALL
SELECT 'ORDERS', COUNT(*), 99441
FROM DBT_BRAZIL.OLIST_RAW.ORDERS
UNION ALL
SELECT 'ORDER_ITEMS', COUNT(*), 112650
FROM DBT_BRAZIL.OLIST_RAW.ORDER_ITEMS
UNION ALL
SELECT 'PRODUCTS', COUNT(*), 32951
FROM DBT_BRAZIL.OLIST_RAW.PRODUCTS
UNION ALL
SELECT 'ORDER_PAYMENTS', COUNT(*), 103886
FROM DBT_BRAZIL.OLIST_RAW.ORDER_PAYMENTS
UNION ALL
SELECT 'PRODUCT_CATEGORY_TRANSLATION', COUNT(*), 71
FROM DBT_BRAZIL.OLIST_RAW.PRODUCT_CATEGORY_TRANSLATION;

-- FALLBACK — if your account cannot create an external access integration:
-- download the six URLs in the FILES list above with a browser or curl, then use
-- Snowsight's Load Data wizard on each table with the OLIST_CSV file format.
-- The COPY INTO statements above become unnecessary; the verification query
-- still applies. Note the wizard matches columns by position, not name — the
-- DDL in Part 1 is already in CSV column order.


-- At this point, switch to the terminal and run the first full build:
--     dbt build --profiles-dir .


-- bad data
-- dbt build --profiles-dir . --select stg_orders+


UPDATE DBT_BRAZIL.OLIST_RAW.ORDERS
SET ORDER_STATUS = 'DELIVERD'
WHERE ORDER_ID = (SELECT MIN(ORDER_ID) FROM DBT_BRAZIL.OLIST_RAW.ORDERS);

SELECT ORDER_ID, ORDER_STATUS
FROM DBT_BRAZIL.OLIST_RAW.ORDERS
WHERE ORDER_STATUS = 'DELIVERD';



-- fix data
-- dbt build --profiles-dir . --select stg_orders+

UPDATE DBT_BRAZIL.OLIST_RAW.ORDERS
SET ORDER_STATUS = 'delivered'
WHERE ORDER_STATUS = 'DELIVERD';

SELECT ORDER_ID, ORDER_STATUS
FROM DBT_BRAZIL.OLIST_RAW.ORDERS
WHERE ORDER_STATUS NOT IN (
    'delivered', 'shipped', 'canceled', 'unavailable',
    'invoiced', 'processing', 'created', 'approved'
);


-- STEP 0 — pick an order still in flight, and note the ID
SELECT ORDER_ID, ORDER_STATUS, ORDER_DELIVERED_CUSTOMER_DATE
FROM DBT_BRAZIL.OLIST_RAW.ORDERS
WHERE ORDER_STATUS = 'shipped'
ORDER BY ORDER_ID
LIMIT 5;


-- STEP 1 — the business change: the order finally reaches the customer.
-- Targets the same row STEP 0 lists first.
UPDATE DBT_BRAZIL.OLIST_RAW.ORDERS
SET ORDER_STATUS = 'delivered',
    ORDER_DELIVERED_CUSTOMER_DATE = CURRENT_TIMESTAMP()
WHERE ORDER_ID = (
    SELECT MIN(ORDER_ID)
    FROM DBT_BRAZIL.OLIST_RAW.ORDERS
    WHERE ORDER_STATUS = 'shipped'
);


-- STEP 2 — both versions now exist in the snapshot.
-- The superseded row has a DBT_VALID_TO; the current row's is NULL.
-- Paste the ORDER_ID noted in STEP 0.
SELECT
    ORDER_ID,
    ORDER_STATUS,
    ORDER_DELIVERED_CUSTOMER_DATE,
    DBT_VALID_FROM,
    DBT_VALID_TO
FROM DBT_BRAZIL.SNAPSHOTS.ORDERS_SNAPSHOT
WHERE ORDER_ID = '<paste the ORDER_ID from STEP 0>'
ORDER BY DBT_VALID_FROM;


-- STEP 3 — current source record vs historical snapshot records, side by side
SELECT
    'CURRENT SOURCE' AS RECORD_SOURCE,
    ORDER_STATUS,
    ORDER_DELIVERED_CUSTOMER_DATE,
    NULL AS DBT_VALID_TO
FROM DBT_BRAZIL.OLIST_RAW.ORDERS
WHERE ORDER_ID = '<paste the ORDER_ID from STEP 0>'

UNION ALL

SELECT
    'SNAPSHOT HISTORY',
    ORDER_STATUS,
    ORDER_DELIVERED_CUSTOMER_DATE,
    DBT_VALID_TO
FROM DBT_BRAZIL.SNAPSHOTS.ORDERS_SNAPSHOT
WHERE ORDER_ID = '<paste the ORDER_ID from STEP 0>';

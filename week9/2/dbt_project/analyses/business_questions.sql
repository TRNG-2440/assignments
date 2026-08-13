-- Business questions answered from the final analytical models only.
-- These are dbt analyses: compiled by dbt, but not materialised. Run the compiled
-- SQL from target/compiled/... in Snowflake, or copy a query out individually.


-- 1. Which product categories contribute the highest sales?
SELECT
    PRODUCT_CATEGORY_NAME_ENGLISH,
    TOTAL_REVENUE,
    TOTAL_ORDERS,
    ITEMS_SOLD
FROM {{ ref('mart_category_performance') }}
ORDER BY TOTAL_REVENUE DESC
LIMIT 10;


-- 2. Which geographical regions contribute the most business?
SELECT
    REGION_NAME,
    SUM(TOTAL_REVENUE) AS REGION_REVENUE,
    SUM(TOTAL_ORDERS) AS REGION_ORDERS,
    SUM(UNIQUE_CUSTOMERS) AS REGION_CUSTOMERS
FROM {{ ref('mart_regional_performance') }}
GROUP BY REGION_NAME
ORDER BY REGION_REVENUE DESC;


-- 3. Which individual states contribute the most business?
SELECT
    CUSTOMER_STATE,
    STATE_NAME,
    REGION_NAME,
    TOTAL_REVENUE,
    TOTAL_ORDERS,
    AVG_FREIGHT_VALUE
FROM {{ ref('mart_regional_performance') }}
ORDER BY TOTAL_REVENUE DESC
LIMIT 10;


-- 4. Which business areas are meeting or missing their target?
SELECT
    PRODUCT_CATEGORY_NAME_ENGLISH,
    PRIORITY_LEVEL,
    TOTAL_REVENUE,
    TARGET_REVENUE,
    REVENUE_VARIANCE,
    TARGET_STATUS
FROM {{ ref('mart_category_target_analysis') }}
WHERE TARGET_STATUS <> 'NO TARGET SET'
ORDER BY REVENUE_VARIANCE DESC;


-- 5. Which high-priority categories are falling short?
SELECT
    PRODUCT_CATEGORY_NAME_ENGLISH,
    TOTAL_REVENUE,
    TARGET_REVENUE,
    REVENUE_VARIANCE
FROM {{ ref('mart_category_target_analysis') }}
WHERE TARGET_STATUS = 'BELOW TARGET'
  AND PRIORITY_LEVEL = 'HIGH'
ORDER BY REVENUE_VARIANCE ASC;


-- 6. What changes can be identified through the snapshot history?
--    The one query that reads outside the marts, because snapshot history is
--    the subject of the question.
SELECT
    ORDER_ID,
    ORDER_STATUS,
    ORDER_DELIVERED_CUSTOMER_DATE,
    DBT_VALID_FROM,
    DBT_VALID_TO,
    CASE
        WHEN DBT_VALID_TO IS NULL THEN 'CURRENT'
        ELSE 'SUPERSEDED'
    END AS VERSION_STATE
FROM {{ ref('orders_snapshot') }}
WHERE ORDER_ID IN (
    SELECT ORDER_ID
    FROM {{ ref('orders_snapshot') }}
    GROUP BY ORDER_ID
    HAVING COUNT(*) > 1
)
ORDER BY ORDER_ID, DBT_VALID_FROM;

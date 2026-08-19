WITH source AS (
    SELECT * FROM {{ source('ecommerce_raw', 'customers')}}
),

renamed AS (
    SELECT 
        customer_id,
        customer_unique_id,
        lpad(customer_zip_code_prefix::VARCHAR, 5, '0') AS customer_zip_code_prefix,
        LOWER(TRIM(customer_city)) AS customer_city,
        UPPER(TRIM(customer_state)) AS customer_state
    FROM source
)

SELECT * FROM renamed
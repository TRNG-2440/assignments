with source as (
    select * from {{ source('ecommerce_raw', 'product_translations') }}
),

renamed as (
    select
        trim(product_category_name) as product_category_name,
        trim(product_category_name_english) as product_category_name_english
    from source
)

select * from renamed
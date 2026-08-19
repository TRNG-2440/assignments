with source as (
    select * from {{ source('ecommerce_raw', 'products') }}
),

renamed as (
    select
        product_id,
        coalesce(nullif(trim(product_category_name), ''), 'unknown')
            as product_category_name,
        product_name_lenght::integer as product_name_length,
        product_description_lenght::integer as product_description_length,
        product_photos_qty::integer as product_photos_qty,
        product_weight_g::number(10, 2) as product_weight_g,
        product_length_cm::number(10, 2) as product_length_cm,
        product_height_cm::number(10, 2) as product_height_cm,
        product_width_cm::number(10, 2) as product_width_cm
    from source
)

select * from renamed
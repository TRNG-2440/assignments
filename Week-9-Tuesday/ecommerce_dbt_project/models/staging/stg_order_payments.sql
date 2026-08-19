with source as (
    select * from {{ source('ecommerce_raw', 'order_payments') }}
),

renamed as (
    select
        order_id,
        payment_sequential::integer as payment_sequential,
        lower(trim(payment_type)) as payment_type,
        payment_installments::integer as payment_installments,
        payment_value::number(10, 2) as payment_value
    from source
)

select * from renamed
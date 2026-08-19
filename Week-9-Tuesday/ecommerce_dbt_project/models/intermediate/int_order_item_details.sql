with order_items as (
    select * from {{ ref('stg_order_items') }}
),

orders as (
    select * from {{ ref('stg_orders') }}
),

customers as (
    select * from {{ ref('stg_customers') }}
),

products as (
    select * from {{ ref('stg_products') }}
),

translations as (
    select * from {{ ref('stg_product_translations') }}
),

order_item_details as (
    select
        oi.order_id,
        oi.order_item_id,
        oi.product_id,
        o.customer_id,
        c.customer_unique_id,
        c.customer_city,
        c.customer_state,
        o.order_status,
        o.order_purchase_at,
        coalesce(t.product_category_name_english, p.product_category_name, 'unknown')
            as product_category_name,
        oi.item_price,
        oi.freight_value,
        oi.item_total
    from order_items oi
    inner join orders o
        on oi.order_id = o.order_id
    inner join customers c
        on o.customer_id = c.customer_id
    left join products p
        on oi.product_id = p.product_id
    left join translations t
        on p.product_category_name = t.product_category_name
    where o.order_status = 'delivered'
)

select * from order_item_details
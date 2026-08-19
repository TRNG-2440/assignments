with order_items as (
    select * from {{ ref('int_order_item_details') }}
),

customer_value as (
    select
        customer_unique_id,
        any_value(customer_city) as customer_city,
        any_value(customer_state) as customer_state,
        count(distinct order_id) as order_count,
        sum(item_price) as lifetime_value,
        round(sum(item_price) / count(distinct order_id), 2) as avg_order_value
    from order_items
    group by customer_unique_id
)

select *
from customer_value
order by lifetime_value desc
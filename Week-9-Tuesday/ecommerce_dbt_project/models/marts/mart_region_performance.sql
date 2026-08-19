with order_items as (
    select * from {{ ref('int_order_item_details') }}
),

regions as (
    select * from {{ ref('region_classifications') }}
),

region_performance as (
    select
        coalesce(r.region_name, 'Unknown') as region_name,
        oi.customer_state,
        count(distinct oi.order_id) as order_count,
        count(distinct oi.customer_unique_id) as customer_count,
        sum(oi.item_price) as total_sales
    from order_items oi
    left join regions r
        on oi.customer_state = r.customer_state
    group by
        coalesce(r.region_name, 'Unknown'),
        oi.customer_state
)

select *
from region_performance
order by total_sales desc
with order_items as (
    select * from {{ ref('int_order_item_details') }}
),

category_sales as (
    select
        product_category_name,
        count(distinct order_id) as order_count,
        count(*) as item_count,
        sum(item_price) as total_sales,
        sum(freight_value) as total_freight,
        sum(item_total) as total_gmv
    from order_items
    group by product_category_name
)

select
    product_category_name,
    order_count,
    item_count,
    total_sales,
    total_freight,
    total_gmv,
    round(100 * total_sales / sum(total_sales) over (), 2) as sales_share_pct
from category_sales
order by total_sales desc
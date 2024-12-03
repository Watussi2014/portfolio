select *
from {{ ref('snow_sales_order_items') }}
where productid != 'RC-1055' and productid != 'RC-1056'
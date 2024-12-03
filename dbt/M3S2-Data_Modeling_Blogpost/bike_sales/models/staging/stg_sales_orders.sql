select
{{ lower_col('raw', 'SalesOrders') }}
from {{ source('raw', 'SalesOrders') }}




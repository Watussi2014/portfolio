select
{{ lower_col('raw', 'SalesOrderItems') }}
from {{ source('raw', 'SalesOrderItems') }}




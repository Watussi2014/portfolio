select
{{ lower_col('raw', 'Employees') }}
from {{ source('raw', 'Employees') }}




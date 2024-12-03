select
{{ lower_col('raw', 'Products') }}
from {{ source('raw', 'Products') }}




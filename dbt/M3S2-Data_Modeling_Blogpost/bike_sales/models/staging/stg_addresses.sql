select
{{ lower_col('raw', 'Addresses') }}
from {{ source('raw', 'Addresses') }}




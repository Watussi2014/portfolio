select
{{ lower_col('raw', 'ProductCategories') }}
from {{ source('raw', 'ProductCategories') }}




select
{{ lower_col('raw', 'ProductCategoryText') }}
from {{ source('raw', 'ProductCategoryText') }}




select
{{ lower_col('raw', 'ProductTexts') }}
from {{ source('raw', 'ProductTexts') }}




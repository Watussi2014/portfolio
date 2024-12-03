select
{{ lower_col('raw', 'BusinessPartners') }}
from {{ source('raw', 'BusinessPartners') }}




select *
from {{ ref('stg_products') }}
where supplier_partnerid != 100000040 and supplier_partnerid != 100000041
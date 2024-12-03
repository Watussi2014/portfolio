select * 
from {{ ref('stg_product_texts') }}
where productid != 'HB-1175' and productid != 'HB-1176'
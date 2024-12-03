select salesorderid,
        salesorderitem,
        productid,
        currency,
        grossamount,
        netamount,
        taxamount,
        quantity,
        quantityunit,
        deliverydate
from {{ ref('stg_sales_order_items') }}
where productid != 'HB-1175' and productid != 'HB-1176'



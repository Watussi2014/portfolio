select o.*,
        i.salesorderitem,
        i.productid,
        i.grossamount as product_grossamount,
        i.netamount as product_netamount,
        i.taxamount as product_taxamount,
        i.quantity as product_qty,
        i.quantityunit as product_qtyunit,
        i.deliverydate,
        b.partner_description,
        b.emailaddress,
        b.phonenumber,
        b.faxnumber,
        b.webaddress,
        b.companyname,
        b.legalform,
        b.currency as partner_currency,
        b.city as partner_city,
        b.postalcode,
        b.street,
        b.building,
        b.address_typename,
        b.country_code,
        b.country_name,
        b.region_code,
        b.region_name,
        b.validity_startdate,
        b.validity_enddate,
        b.latitude,
        b.longitude
from {{ ref('star_sales_orders') }} o 
join {{ ref('star_sales_order_items') }} i 
    on o.salesorderid = i.salesorderid
join {{ ref('obt_business_partners') }} b 
    on o.partnerid = b.partnerid
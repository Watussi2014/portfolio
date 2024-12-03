select p.productid,
        p.typecode,
        type.typename,
        p.createdby,
        p.createdat,
        p.changedby,
        p.changedat,
        p.supplier_partnerid,
        t.taxtariffcode,
        t.tax_pct,
        p.quantityunit,
        p.weightmeasure,
        p.weightunit,
        p.currency,
        p.price,
        p.width,
        p.depth,
        p.height,
        p.dimensionunit,
        p.productpicurl,
        text.language,
        text.short_descr,
        text.medium_descr,
        text.long_descr,
        p.prodcategoryid,
        pct.language as cat_language,
        pct.short_descr as cat_short_descr,
        pct.medium_descr as cat_medium_descr,
        pct.long_descr as cat_long_descr

from {{ ref('snow_products') }} p
left join {{ ref('snow_prod_tax') }} t 
    on p.taxtariffcode = t.taxtariffcode
left join {{ ref('snow_prod_type') }} type 
    on p.typecode = type.typecode
left join {{ ref('snow_product_texts') }} as text 
    on p.productid = text.productid
left join {{ ref('snow_product_categories') }} as pc 
    on p.prodcategoryid = pc.prodcategoryid
left join {{ ref('snow_product_category_text') }} as pct 
    on pc.prodcategoryid = pct.prodcategoryid

where p.productid != 'RC-1055' and p.productid != 'RC-1056'
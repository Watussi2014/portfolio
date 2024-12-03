{{
  config(
    materialized = 'ephemeral',
    )
}}

select b.partnerid,
        b.partner_description,
        b.emailaddress,
        b.phonenumber,
        b.faxnumber,
        b.webaddress,
        b.companyname,
        b.legalform,
        b.currency,
        b.createdby,
        b.createdat,
        b.changedby,
        b.changedat,
        a.*
from {{ ref('star_business_partners') }} b
join {{ ref('star_addresses') }} a 
    on a.addressid = b.addressid
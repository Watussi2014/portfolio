select b.partnerid,
        r.description as partner_description,
        b.emailaddress,
        b.phonenumber,
        b.faxnumber,
        b.webaddress,
        b.addressid,
        b.companyname,
        b.legalform,
        b.createdby,
        b.createdat,
        b.changedby,
        b.changedat,
        b.currency
from {{ ref('snow_business_partners') }} b
join {{ ref('snow_partner_roles') }} r
    on b.partnerrole = r.partnerrole
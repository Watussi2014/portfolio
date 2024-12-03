select addressid,
        city,
        postalcode,
        street,
        building,
        t.typename as address_typename,
        c.country_code,
        c.country_name,
        r.region_code,
        r.region_name,
        validity_startdate,
        validity_enddate,
        latitude,
        longitude

from {{ ref('snow_addresses') }} a
join {{ ref('snow_address_type') }} t
    on a.addresstype = t.addresstype
join {{ ref('snow_countries') }} c
    on a.country_code = c.country_code
join {{ ref('snow_region') }} r
    on c.region_code = r.region_code
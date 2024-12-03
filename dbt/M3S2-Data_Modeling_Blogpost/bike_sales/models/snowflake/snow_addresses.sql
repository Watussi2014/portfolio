select addressid,
        city,
        postalcode,
        street,
        building,
        addresstype,
        country as country_code,
        validity_startdate,
        validity_enddate,
        latitude,
        longitude
from {{ ref('stg_addresses') }}

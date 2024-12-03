with drivers as (
    select *
    from {{ source('raw', 'drivers') }}
)

select "driverId"::smallint as driver_id,
        "driverRef" as driver_ref,
        number,
        code,
        forename,
        surname,
        {{convert_type("dob", 'date')}} as dob,
        nationality
        
from drivers





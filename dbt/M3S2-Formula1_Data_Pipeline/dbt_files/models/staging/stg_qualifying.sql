with qualifying as (
    select *
    from {{ source('raw', 'qualifying') }}
)

select "qualifyId"::integer as qualify_id,
        "raceId"::integer as race_id,
        "driverId"::smallint as driver_id,
        "constructorId"::smallint as constructor_id,
        number,
        position::smallint,
        {{convert_type("q1",'time')}} as q1,
        {{convert_type("q2",'time')}} as q2,
        {{convert_type("q3",'time')}} as q3
        
from qualifying





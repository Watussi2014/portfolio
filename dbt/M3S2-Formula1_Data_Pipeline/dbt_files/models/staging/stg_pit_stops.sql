with pit_stops as (
    select *
    from {{ source('raw', 'pit_stops') }}
)

select "raceId"::integer as race_id,
        "driverId"::smallint as driver_id,
        stop::smallint,
        lap::smallint,
        {{convert_type("time", 'time')}} as time,
        duration,
        milliseconds
        
from pit_stops





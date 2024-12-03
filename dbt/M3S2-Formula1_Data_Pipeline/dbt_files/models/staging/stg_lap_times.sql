with lap_times as (
    select *
    from {{ source('raw', 'lap_times') }}
)

select "raceId"::integer as race_id,
        "driverId"::smallint as driver_id,
        lap::smallint,
        position::smallint,
        time,
        milliseconds
from lap_times





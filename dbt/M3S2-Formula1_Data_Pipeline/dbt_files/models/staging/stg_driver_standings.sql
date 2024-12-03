with driver_standings as (
    select *
    from {{ source('raw', 'driver_standings') }}
)

select "driverStandingsId"::integer as driver_standings_id,
        "raceId"::integer as race_id,
        "driverId"::smallint as driver_id,
        points,
        position::smallint,
        "positionText" as position_text,
        wins::smallint
        
from driver_standings





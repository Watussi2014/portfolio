with results as (
    select *
    from {{ source('raw', 'results') }}
),

status as (
    select *
    from {{ source('raw', 'status') }}
)

select "resultId"::integer as result_id, 
        "raceId"::integer as race_id,
        "driverId"::smallint as driver_id,
        "constructorId"::smallint as constructor_id,
        number,
        grid,
        {{convert_type("position",'smallint')}} as position,
        "positionText" as position_text,
        "positionOrder"::smallint as position_order,
        points,
        laps::smallint,
        time,
        milliseconds,
        "fastestLap" as fastest_lap,
        rank,
        {{convert_type("fastestLapTime", 'time')}} as fastest_lap_time,
        {{convert_type("fastestLapSpeed", 'double precision')}} as fastest_lap_speed,
        s.status
        
from results r
join status s using ("statusId")





with constructor_standings as (
    select *
    from {{ source('raw', 'constructor_standings') }}
)

select "constructorStandingsId"::smallint as constructor_standings_id,
        "raceId"::integer as race_id,
        "constructorId"::smallint as constructor_id,
        points,
        position::smallint,
        "positionText" as position_text,
        wins::smallint
from constructor_standings 


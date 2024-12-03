with races as (
    select *
    from {{ source('raw', 'races') }}
)

select "raceId"::integer as race_id,
        year::smallint,
        round::smallint,
        "circuitId"::smallint as circuit_id,
        name,
        TO_DATE("date"::TEXT, 'YYYY-MM-DD') as date,
        {{convert_type("time", 'time')}} as time,
        {{convert_type("fp1_date", 'date')}} as fp1_date,
        {{convert_type("fp1_time", 'time')}} as fp1_time,
        {{convert_type("fp2_date", 'date')}} as fp2_date,
        {{convert_type("fp2_time", 'time')}} as fp2_time,
        {{convert_type("fp3_date", 'date')}} as fp3_date,
        {{convert_type("fp3_time", 'time')}} as fp3_time,
        {{convert_type("quali_date", 'date')}} as quali_date,
        {{convert_type("quali_time", 'time')}} as quali_time,
        {{convert_type("sprint_date", 'date')}} as sprint_date,
        {{convert_type("sprint_time", 'time')}} as sprint_time
        
from races





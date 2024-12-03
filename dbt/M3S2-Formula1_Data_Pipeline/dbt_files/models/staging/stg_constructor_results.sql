with constructor_results as (
    select *
    from {{ source('raw', 'constructor_results') }}
)


select "constructorResultsId"::smallint as constructor_results_id,
        "raceId"::integer as race_id,
        "constructorId"::smallint as constructor_id,
        points,
        CASE WHEN "status" = '\N' THEN NULL ELSE "status" END as status 
from constructor_results



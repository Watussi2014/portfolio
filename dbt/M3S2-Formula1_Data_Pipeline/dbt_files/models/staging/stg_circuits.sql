with circuits as (
    select *
    from {{ source('raw', 'circuits') }}
)

select "circuitId"::smallint as circuit_id,
        "circuitRef" as circuit_ref,
        name,
        location,
        country,
        lat,
        lng,
        alt::integer
        
from circuits





with constructors as (
    select *
    from {{ source('raw', 'constructors') }}
)

select "constructorId"::smallint as constructor_id,
        "constructorRef" as constructor_ref,
        name,
        nationality
from constructors

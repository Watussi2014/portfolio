with results as (
    select *
    from {{ ref('stg_results') }}
),

qualifying as (
    select *
    from {{ ref('stg_qualifying') }}
)

select r.*,
        q.position as starting_grid_position
from results r
join qualifying q on r.race_id = q.race_id and r.driver_id = q.driver_id
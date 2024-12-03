with races as (
    select *
    from {{ ref('stg_races') }}
),

results as (
    select *
    from {{ ref('stg_results') }}
),

drivers as (
    select *
    from {{ ref('stg_drivers') }}
),

circuits as (
    select *
    from {{ ref('stg_circuits') }}
),

qualifying as (
    select *
    from {{ ref('stg_qualifying') }}
),

constructors as (
    select *
    from {{ ref('stg_constructors') }}
)


SELECT  r.race_id,
        r.name AS race_name,
        r.circuit_id,
        c.name AS circuit_name,
        r.date,
        r.year,
        r.round,
        q.driver_id AS pole_driver_id,
        q.constructor_id AS pole_constructor_id,
        q.code AS pole_code,
        q.q3 as q3_time,
        re.driver_id AS winner_driver_id,
        d.code AS winner_code,
        re.time as winner_time,
        re.constructor_id AS winner_constructor_id,
        re.name AS winner_constructor
        

FROM races r

JOIN ( -- Filtering only the winner for each races
    SELECT re.race_id, re.driver_id, re.time, re.constructor_id, c.name
    FROM results re
    JOIN constructors c ON c.constructor_id = re.constructor_id
    WHERE re.position = '1'
) re ON re.race_id = r.race_id

JOIN drivers d ON d.driver_id = re.driver_id
JOIN circuits c ON c.circuit_id = r.circuit_id

JOIN ( -- Finding the q3 pole driver code
    SELECT q.race_id, q.driver_id, q.q3, d.code, q.constructor_id
    FROM qualifying q
    JOIN drivers d ON q.driver_id = d.driver_id
    WHERE q.position = 1
    ) q ON q.race_id = r.race_id



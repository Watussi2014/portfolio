with source as (
    select *
    from {{ ref('clean_data') }}
    where competition_name = 'UEFA Champions League'
            and stage = 'LEAGUE_STAGE'
),

{{ get_league_table()}}
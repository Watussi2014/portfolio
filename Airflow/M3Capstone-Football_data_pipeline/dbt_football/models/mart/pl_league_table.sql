with source as (
    select *
    from {{ ref('clean_data') }}
    where competition_name = 'Premier League'
),

{{ get_league_table()}}
with source as (
    select *
    from {{ ref('clean_data') }}
    where competition_name = 'Bundesliga'
),

{{ get_league_table()}}
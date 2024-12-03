with source as (
    select *
    from {{ ref('clean_data') }}
    where competition_name = 'Serie A'
),

{{ get_league_table()}}
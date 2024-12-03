with source as (
    select *
    from {{ ref('clean_data') }}
    where competition_name = 'Primera Division'
),

{{ get_league_table()}}
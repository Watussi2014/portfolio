{% macro get_league_table() %}

results as (
    select home_team_name as team, 
            winner,
            home_team_score as goals_for,
            away_team_score as goals_against

    from source

    union all

    select away_team_name as team, 
            winner,
            away_team_score as goals_for,
            home_team_score as goals_against
    from source
),

result_table as (

select team,
        count(*) as matches_played,
        COUNT(CASE WHEN team = winner THEN 1 END) AS wins,
        COUNT(CASE WHEN winner = 'DRAW' THEN 1 END) AS draws,
        COUNT(CASE WHEN team != winner AND winner != 'DRAW' THEN 1 END) AS loses,
        SUM(goals_for) as goals_for,
        SUM(goals_against) as goals_against
from results
group by team
)

select *,
        (wins*3) + (draws*1) as points,
        goals_for - goals_against as goal_differences
from result_table
order by points desc, goal_differences desc

{% endmacro %}
select  distinct id,
        competition_name,
        utc_date::timestamp,
        matchday::smallint,
        stage,
        home_team_name,
        home_team_tla,
        away_team_name,
        away_team_tla,
        case when winner = 'HOME_TEAM' THEN  home_team_name
                when winner = 'AWAY_TEAM' THEN away_team_name
                else winner end as winner,
        duration,
        home_team_score::smallint,
        away_team_score::smallint

from {{ source('raw', 'matches_data') }}
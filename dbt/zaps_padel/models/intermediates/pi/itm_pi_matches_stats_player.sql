{{ config(
    partition_by = {
      "field": "created_at",
      "data_type": "date",
      "granularity": "day"
    },
    materialized = 'materialized_view',
    on_configuration_change = 'apply',
    enable_refresh=true,
    refresh_interval_minutes=240
)}}

SELECT 
    created_at,
    matchId,
    'Match' AS matchPeriod,
    STRUCT(
      team1Left,
      team1Right    
    ) AS team1,
    STRUCT(
      team2Left,
      team2Right    
    ) AS team2  
FROM 
    {{ ref('stg_pi_matches_stats_player') }}
UNION ALL
SELECT 
    created_at,
    matchId,
    CASE setNum
        WHEN 1 THEN 'Set 1'
        WHEN 2 THEN 'Set 2'
        WHEN 3 THEN 'Set 3'
    ELSE NULL
    END AS matchPeriod,
    STRUCT(
      playerStats.team1Left,
      playerStats.team1Right    
    ) AS team1,
    STRUCT(
      playerStats.team2Left,
      playerStats.team2Right    
    ) AS team2  
FROM
    {{ ref('stg_pi_matches_stats_sets') }}
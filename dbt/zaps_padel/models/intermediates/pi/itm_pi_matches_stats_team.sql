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
      pointsWon.team1 AS pointsWon,
      breakPointsAttempts.team1 AS breakPointsAttempts,
      breakPointsWon.team1 AS breakPointsWon,
      winners.team1 AS winners,
      uErrors.team1 AS uErrors
    ) AS team1,
    STRUCT(
      pointsWon.team2 AS pointsWon,
      breakPointsAttempts.team2 AS breakPointsAttempts,
      breakPointsWon.team2 AS breakPointsWon,
      winners.team2 AS winners,
      uErrors.team2 AS uErrors
    ) AS team2
FROM 
    {{ ref('stg_pi_matches_stats_team') }}
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
      teamStats.pointsWon.team1 AS pointsWon,
      teamStats.breakPointsAttempts.team1 AS breakPointsAttempts,
      teamStats.breakPointsWon.team1 AS breakPointsWon,
      teamStats.winners.team1 AS winners,
      teamStats.uErrors.team1 AS uErrors
    ) AS team1,
    STRUCT(
      teamStats.pointsWon.team2 AS pointsWon,
      teamStats.breakPointsAttempts.team2 AS breakPointsAttempts,
      teamStats.breakPointsWon.team2 AS breakPointsWon,
      teamStats.winners.team2 AS winners,
      teamStats.uErrors.team2 AS uErrors
    ) AS team2
FROM
    {{ ref('stg_pi_matches_stats_sets') }}
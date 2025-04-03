{{ config(
    partition_by = {
      "field": "created_at",
      "data_type": "date",
      "granularity": "day"
    },
    materialized = 'incremental',
    on_schema_change = 'append_new_columns'
)}}

{% if is_incremental() %}
  {% set max_created_at = run_query("SELECT MAX(created_at) FROM " ~ this).columns[0][0] or '2025-01-01' %}
{% endif %}

SELECT 
  date AS created_at,
  match.id AS matchId,
  setNum,
  match.team1Left.id AS team1LeftPlayerId,
  match.team1Right.id AS team1RightPlayerId,
  match.team2Left.id AS team2LeftPlayerId,
  match.team2Right.id AS team2RightPlayerId,
  lastPointsStats.longestPoint,
  lastPointsStats.rallyLengthAvg,
  teamStats,
  STRUCT(
    {{ player_stats_struct('playerStats.team1Left','team1Left') }},
    {{ player_stats_struct('playerStats.team1Right','team1Right') }},
    {{ player_stats_struct('playerStats.team2Left','team2Left') }}, 
    {{ player_stats_struct('playerStats.team2Right','team2Right') }}  
  ) AS playerStats
FROM 
    {{ source('padel_intelligence','raw_pi_matches_stats_sets') }}
WHERE 
  {% if is_incremental() %}
    date > '{{ max_created_at }}'
  {% else %}
    date >= '2025-01-01'
  {% endif %}
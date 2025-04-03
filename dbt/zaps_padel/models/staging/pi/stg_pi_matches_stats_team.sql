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
    matchId,
    team1,
    team2,
    pointsWon,
    breakPointsAttempts,
    breakPointsWon,
    goldenPointsAgainst,
    goldenPointsWon,
    winners,
    uErrors
FROM 
    {{ source('padel_intelligence','raw_pi_matches_stats_team') }}
WHERE 
  {% if is_incremental() %}
    date > '{{ max_created_at }}'
  {% else %}
    date >= '2025-01-01'
  {% endif %}
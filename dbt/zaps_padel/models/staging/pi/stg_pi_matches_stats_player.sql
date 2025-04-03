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
    {{ player_stats_struct('team1Left','team1Left') }},
    {{ player_stats_struct('team1Right','team1Right') }},
    {{ player_stats_struct('team2Left','team2Left') }}, 
    {{ player_stats_struct('team2Right','team2Right') }}  
FROM 
    {{ source('padel_intelligence','raw_pi_matches_stats_player') }}
WHERE 
  {% if is_incremental() %}
    date > '{{ max_created_at }}'
  {% else %}
    date >= '2025-01-01'
  {% endif %}
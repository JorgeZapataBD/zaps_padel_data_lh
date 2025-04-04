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
  created_at,
  id,
  startTime as match_date,
  tournament.id AS tournament_id,
  matchRound as match_round,
  team1Left.id as team1_left_player_id,
  team1Right.id as team1_right_player_id,
  team2Left.id as team2_left_player_id,
  team2Right.id as team2_right_player_id,
FROM
  {{ ref('stg_pi_matches_list') }}
{% if is_incremental() %}
WHERE
    created_at > '{{ max_created_at }}'
{% endif %}
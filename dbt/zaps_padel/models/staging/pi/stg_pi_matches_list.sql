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
    id,
    SAFE.PARSE_DATETIME('%Y-%m-%dT%H:%M:%E3SZ', startTime) AS startTime,
    tiebreak,
    goldenPoint,
    matchRound,
    tournament,
    team1Left,
    team1Right,
    team2Left,
    team2Right
FROM 
    {{ source('padel_intelligence','raw_pi_matches_list') }}
WHERE 
  {% if is_incremental() %}
    date > '{{ max_created_at }}'
  {% else %}
    date >= '2025-01-01'
  {% endif %}
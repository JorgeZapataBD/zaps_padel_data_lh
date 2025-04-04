{{ config(
    partition_by = {
      "field": "created_at",
      "data_type": "date",
      "granularity": "day"
    },
    materialized = 'incremental',
    unique_key = 'id',
    incremental_strategy = 'merge',
    on_schema_change = 'append_new_columns'
)}}

{% if is_incremental() %}
  {% set max_created_at = run_query("SELECT MAX(created_at) FROM " ~ this).columns[0][0] or '2025-01-01' %}
{% endif %}

WITH player_data AS (
  SELECT 
    created_at,
    tournament.id,
    tournament.name,
    tournament.description,
    tournament.location,
    tournament.tour,
    tournament.goldenPoint,
    ROW_NUMBER() OVER (PARTITION BY tournament.id ORDER BY created_at DESC) AS rn
  FROM 
    {{ ref('stg_pi_matches_list') }}
  {% if is_incremental() %}
  WHERE
    created_at > '{{ max_created_at }}'
  {% endif %}
)
SELECT 
    *EXCEPT(rn)
FROM 
    player_data
WHERE 
    rn = 1
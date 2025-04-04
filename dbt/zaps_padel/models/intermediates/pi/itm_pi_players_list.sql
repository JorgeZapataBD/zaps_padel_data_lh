{{ config(
    partition_by = {
      "field": "created_at",
      "data_type": "date",
      "granularity": "day"
    },
    materialized = 'incremental',
    unique_key = 'id',
    incremental_strategy = 'merge',
    merge_updated_columns = ['brand_id', 'brand_name', 'preferSide','created_at'],
    on_schema_change = 'append_new_columns'
)}}

{% if is_incremental() %}
  {% set max_created_at = run_query("SELECT MAX(created_at) FROM " ~ this).columns[0][0] or '2025-01-01' %}
{% endif %}

WITH player_data AS (
  SELECT 
    created_at,
    player.id,
    player.name,
    player.nickname,
    SAFE.PARSE_DATE('%Y-%m-%d', player.birthdate) AS birthdate,
    player.hand,
    player.preferSide,
    player.country,
    player.gender,
    player.brand.id AS brand_id,
    player.brand.name AS brand_name,
    ROW_NUMBER() OVER (PARTITION BY player.id ORDER BY created_at DESC) AS rn
  FROM 
    {{ ref('stg_pi_matches_list') }}
  UNPIVOT(
      player FOR position IN (team1Left, team1Right, team2Left, team2Right)
  )
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
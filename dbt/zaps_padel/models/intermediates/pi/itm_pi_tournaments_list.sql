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

WITH tournament_data AS (
  SELECT 
    created_at,
    tournament.id,
    SAFE_CAST(TRIM(SPLIT(TRANSLATE(UPPER(tournament.name), 'ÁÉÍÓÚÑ', 'AEIOUN'), ' - ')[SAFE_OFFSET(1)]) AS INT64) AS seasonId,
    TRIM(SPLIT(TRANSLATE(UPPER(tournament.name), 'ÁÉÍÓÚÑ', 'AEIOUN'), ' - ')[SAFE_OFFSET(0)]) AS name,
    TRANSLATE(UPPER(tournament.description), 'ÁÉÍÓÚÑ', 'AEIOUN') AS description,
    CASE
      WHEN TRIM(SPLIT(TRANSLATE(UPPER(tournament.name), 'ÁÉÍÓÚÑ', 'AEIOUN'), ' - ')[SAFE_OFFSET(0)]) LIKE '%P1' THEN 'P1'
      WHEN TRIM(SPLIT(TRANSLATE(UPPER(tournament.name), 'ÁÉÍÓÚÑ', 'AEIOUN'), ' - ')[SAFE_OFFSET(0)]) LIKE '%P2' THEN 'P2'
      WHEN TRIM(SPLIT(TRANSLATE(UPPER(tournament.name), 'ÁÉÍÓÚÑ', 'AEIOUN'), ' - ')[SAFE_OFFSET(0)]) LIKE '%MAJOR%' THEN 'MAJOR'
      WHEN TRIM(SPLIT(TRANSLATE(UPPER(tournament.name), 'ÁÉÍÓÚÑ', 'AEIOUN'), ' - ')[SAFE_OFFSET(0)]) LIKE '%FINALS%' THEN 'FINALS'    
      ELSE NULL
    END AS level,
    UPPER(tournament.location) AS country,
    tournament.tour,
    tournament.goldenPoint,
    ROW_NUMBER() OVER (PARTITION BY tournament.id ORDER BY created_at DESC) AS rn
  FROM 
    {{ ref('stg_pi_matches_list') }}
  WHERE
    tournament.tour.id = 3
  {% if is_incremental() %}
    AND created_at > '{{ max_created_at }}'
  {% endif %}
)
SELECT 
    *EXCEPT(rn)
FROM 
    tournament_data
WHERE 
    rn = 1
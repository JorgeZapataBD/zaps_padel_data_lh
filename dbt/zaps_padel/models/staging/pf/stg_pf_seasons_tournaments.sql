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
    EXTRACT(YEAR FROM SAFE.PARSE_DATE('%Y-%m-%d', start_date)) AS season_id,
    TRANSLATE(UPPER(name), 'ÁÉÍÓÚÑ', 'AEIOUN') AS name,
    TRANSLATE(UPPER(location), 'ÁÉÍÓÚÑ', 'AEIOUN') AS location,
    country AS country_id,
    UPPER(level) AS level,
    SAFE.PARSE_DATE('%Y-%m-%d', start_date) AS start_date,
    SAFE.PARSE_DATE('%Y-%m-%d', end_date) AS end_date
FROM 
    {{ source('padel_fantasy','raw_pf_seasons_tournaments') }}
WHERE 
  SAFE.PARSE_DATE('%Y-%m-%d', start_date) >= '2024-01-01'
  {% if is_incremental() %}
    AND date > '{{ max_created_at }}'
  {% else %}
    AND date >= '2025-01-01'
  {% endif %}
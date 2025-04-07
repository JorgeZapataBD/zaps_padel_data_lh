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
    name,
    location,
    country,
    level,
    SAFE.PARSE_DATE('%Y-%m-%d', start_date) AS start_date,
    SAFE.PARSE_DATE('%Y-%m-%d', end_date) AS end_date
FROM 
    {{ source('padel_fantasy','raw_pf_seasons_tournaments') }}
WHERE 
  {% if is_incremental() %}
    date > '{{ max_created_at }}'
  {% else %}
    date >= '2025-01-01'
  {% endif %}
{% macro player_stats_struct(struct_col, struct_name) %}
    STRUCT(
      SAFE_CAST({{ struct_col }}.assists AS INT64) AS assists,
      SAFE_CAST({{ struct_col }}.netRegains AS INT64) AS netRegains,
      SAFE_CAST({{ struct_col }}.pErrors AS INT64) AS pErrors,
      SAFE_CAST({{ struct_col }}.participation AS FLOAT64) AS participation,
      SAFE_CAST({{ struct_col }}.pi AS FLOAT64) AS pi,
      SAFE_CAST({{ struct_col }}.piKp AS FLOAT64) AS piKp,
      SAFE_CAST({{ struct_col }}.returnTotal AS INT64) AS returnTotal,
      SAFE_CAST({{ struct_col }}.returnWon AS INT64) AS returnWon,
      SAFE_CAST({{ struct_col }}.returnWonPercentage AS FLOAT64) AS returnWonPercentage,
      SAFE_CAST({{ struct_col }}.rulos AS INT64) AS rulos,
      SAFE_CAST({{ struct_col }}.serverTotal AS INT64) AS serverTotal,
      SAFE_CAST({{ struct_col }}.serverWon AS INT64) AS serverWon,
      SAFE_CAST({{ struct_col }}.serverWonPercentage AS FLOAT64) AS serverWonPercentage,
      SAFE_CAST({{ struct_col }}.smashAttempts AS INT64) AS smashAttempts,
      SAFE_CAST({{ struct_col }}.smashWinners AS INT64) AS smashWinners,
      SAFE_CAST({{ struct_col }}.uErrors AS INT64) AS uErrors,
      SAFE_CAST({{ struct_col }}.winners AS INT64) AS winners,
      (SELECT ARRAY(SELECT a.element FROM UNNEST({{ struct_col }}.piHistory.list) AS sublist, UNNEST(sublist.element.list) as a)) AS piHistory
    ) AS {{ struct_name }}
{% endmacro %}
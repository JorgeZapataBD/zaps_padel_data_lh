{% macro player_stats_struct(struct_col, struct_name) %}
    STRUCT(
      {{ struct_col }}.player,
      {{ struct_col }}.assists,
      {{ struct_col }}.netRegains,
      {{ struct_col }}.pErrors,
      {{ struct_col }}.participation,
      {{ struct_col }}.pi,
      {{ struct_col }}.piKp,
      {{ struct_col }}.returnTotal,
      {{ struct_col }}.returnWon,
      {{ struct_col }}.returnWonPercentage,
      {{ struct_col }}.rulos,
      {{ struct_col }}.serverTotal,
      {{ struct_col }}.serverWon,
      {{ struct_col }}.serverWonPercentage,
      {{ struct_col }}.smashAttempts,
      {{ struct_col }}.smashWinners,
      {{ struct_col }}.uErrors,
      {{ struct_col }}.winners,
      (SELECT ARRAY(SELECT a.element FROM UNNEST({{ struct_col }}.piHistory.list) AS sublist, UNNEST(sublist.element.list) as a)) AS piHistory
    ) AS {{ struct_name }}
{% endmacro %}
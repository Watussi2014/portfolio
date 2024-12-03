{% macro lower_col(schema, table_name) %}
-- Transform the columns name into lowercased version of the name

{% set columns = adapter.get_columns_in_relation(source(schema, table_name)) -%}
{%- for col in columns -%}
    "{{ col.name }}" as {{col.name.lower()}}
    {%- if not loop.last -%}, {% endif %}
  {% endfor -%}

{% endmacro %}
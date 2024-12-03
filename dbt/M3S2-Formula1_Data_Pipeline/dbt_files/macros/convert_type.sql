{% macro convert_type(column_name, data_type) %}
    CASE 
        WHEN "{{ column_name }}" = '\N' THEN NULL
        ELSE CAST("{{ column_name }}" AS {{ data_type }})
    END
{% endmacro %}
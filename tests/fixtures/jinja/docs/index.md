# Test page

This is a table that we load from the docs folder, because we set `data_path` to `docs`:

## Dynamically insert a list of tables using jinja2


{% set table_names = ["basic_table.csv","basic_table2.csv"] %}
{% for table_name in table_names %}

### table `{{ table_name }}`

{{ read_csv(table_name) }}

{% endfor %}

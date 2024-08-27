# Test page

This is a table that we load from the docs folder, because we set `data_path` to `docs`:

## Dynamically insert a list of tables using jinja2


{% set table_names = ["basic_table.csv","basic_table2.csv"] %}
{% for table_name in table_names %}

### table `{{ table_name }}`

{{ read_csv(table_name) }}

{% endfor %}


## Now with tabs


{% for table_name in table_names %}

=== "{{ table_name }}"

    {{ read_csv(table_name) | add_indentation(spaces=4) }}


{% endfor %}

## Filtering results

{% raw %}
```
{{ pd_read_csv("numeric_table.csv").query("a >= 3") | convert_to_md_table }}
```
{% endraw %}

{{ pd_read_csv("numeric_table.csv").query("a >= 3") | convert_to_md_table }}


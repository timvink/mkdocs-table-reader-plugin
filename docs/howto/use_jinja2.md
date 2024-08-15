# Using jinja2

`table-reader` supports [`mkdocs-macros-plugin`](https://mkdocs-macros-plugin.readthedocs.io/en/latest/), which enables you to use jinja2 syntax inside markdown files (among other things).

To enable `macros`, specify the plugin _before_ `table-reader` in your `mkdocs.yml` file:

```yaml
plugins:
    - macros
    - table-reader
```

Now you can do cool things like dynamically load a list of tables:


```markdown
# index.md

{% set table_names = ["basic_table.csv","basic_table2.csv"] %}
{% for table_name in table_names %}

{{  read_csv(table_name) }}

{% endfor %}

```
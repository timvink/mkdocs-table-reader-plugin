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

{ { read_csv(table_name) }}

{% endfor %}

```

## Indented content like content tabs

If you inserted content has multiple lines, then indentation will be not be retained beyond the first line. This means things like [content tabs](https://squidfunk.github.io/mkdocs-material/reference/content-tabs/#usage) will not work as expected.

To fix that, you can use the custom _filter_ `add_indendation` (a filter add to `macros` by `table-reader` plugin). For example:

=== "index.md"

    ```jinja
    {% set table_names = ["basic_table.csv","basic_table2.csv"] %}
    {% for table_name in table_names %}

    === "{{ table_name }}"

        { { read_csv(table_name) | add_indentation(spaces=4) }}

    {% endfor %}
    ```

=== "mkdocs.yml"

    ```yaml
    site_name: test git_table_reader site
    use_directory_urls: true

    theme:
    name: material

    plugins:
        - search
        - macros
        - table-reader

    markdown_extensions:
        - pymdownx.superfences
        - pymdownx.tabbed:
            alternate_style: true
    ``` 

!!! note "Note the space in { {"

    To avoid the tables being inserted into the code example, we replaced `{{` with `{ {`.
    If you copy this example, make sure to fix.


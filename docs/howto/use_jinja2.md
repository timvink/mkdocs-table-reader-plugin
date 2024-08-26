# Use jinja2 for automation

`table-reader` supports [`mkdocs-macros-plugin`](https://mkdocs-macros-plugin.readthedocs.io/en/latest/), which enables you to use jinja2 syntax inside markdown files (among other things).

To enable `macros`, specify the plugin _before_ `table-reader` in your `mkdocs.yml` file:

```yaml
plugins:
    - macros
    - table-reader
```

Now you can do cool things like:

## Dynamically load a list of tables

```markdown
# index.md

{% set table_names = ["basic_table.csv","basic_table2.csv"] %}
{% for table_name in table_names %}

{ { read_csv(table_name) }}

{% endfor %}
```

## Insert tables into content tabs

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


## Recursively insert an entire directory of tables

[`mkdocs-macros-plugin`](https://mkdocs-macros-plugin.readthedocs.io/en/latest/) enables you to define additional functions (called _macros_) that you will be able to use within your markdown files.
See their documentation on how to set this up. Here's an example with some functions to interact with the filesystem:

```python
def define_env(env):
    """
    Register additional mkdocs-macros-plugin functions that can be used as macros in markdown files.
    """    
    @env.macro
    def listdir(path):
        return os.listdir(path)
    
    @env.macro
    def path_exists(path):
        return Path(path).exists()

    @env.macro
    def is_file(path):
        return Path(path).is_file() 
```

Now you could do something like:

```markdown
# index.md

{% for table_name in listdir('docs/assets/my_tables") %}

{ { read_csv(table_name) }}

{% endfor %}
```

!!! note "Note the space in { {"

    To avoid the tables being inserted into the code example, we replaced `{{` with `{ {`.
    If you copy this example, make sure to fix.
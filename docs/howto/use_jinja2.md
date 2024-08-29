# Compatibility with mkdocs-macros-plugin to enable further automation

{% raw %}

`table-reader` supports [`mkdocs-macros-plugin`](https://mkdocs-macros-plugin.readthedocs.io/en/latest/), which enables you to use jinja2 syntax inside markdown files (among other things).

To enable `macros`, specify the plugin _before_ `table-reader` in your `mkdocs.yml` file:

```yaml
plugins:
    - macros
    - table-reader
```

Everything will work as before, _except_ indentation will not be retrained. This means components that rely on indentation (like [Admonitions](https://squidfunk.github.io/mkdocs-material/reference/admonitions/) and [Content tabs](https://squidfunk.github.io/mkdocs-material/reference/content-tabs/#usage)) will break.

The solution is to use the custom _filter_ `add_indendation` (a filter added to `macros` by `table-reader` plugin, see the [readers](../readers.md)). For example:

```jinja
!!! note "This is a note"

    {{ read_csv("basic_table.csv") | add_indentation(spaces=4) }}
```

The upside is you now have much more control. A couple of example use cases:

## Dynamically load a specified list of tables into tabs

=== "index.md"

    ```jinja
    {% set table_names = ["basic_table.csv","basic_table2.csv"] %}
    {% for table_name in table_names %}

    === "{{ table_name }}"

        {{ read_csv(table_name) | add_indentation(spaces=4) }}

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

{{ read_csv(table_name) }}

{% endfor %}
```

## Filter a table before inserting it

When you enable the `macros` plugin in your `mkdocs.yml`, `table-reader` will add additional _macros_ and _filters_ (see the [readers overview](../readers.md)).

You can use the `pd_<reader>` variants to read a file to a pandas dataframe. Then you can use the pandas methods like [`.query()`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.query.html). For example:

```
{{ pd_read_csv("numeric_table.csv").query("column_name >= 3") | convert_to_md_table }}
```

{% endraw %}

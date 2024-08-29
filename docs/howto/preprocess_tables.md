# Preprocess input tables

{% raw %}

`mkdocs>=1.4` supports [hooks](https://www.mkdocs.org/user-guide/configuration/#hooks), which enable you to run python scripts on `mkdocs serve` or `mkdocs build`.

Here are some example of workflows that use hooks and the `table-reader` plugin:

## Combine a directory of tables into a single, larger table.

=== "hooks.py"

    ```python
    from os import listdir
    from os.path import isfile, join
    import pandas as pd

    def on_pre_build(config, **kwargs) -> None:
        tables = []
        input_files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        for table in input_files:
            tables.append(pd.read_csv(table))
        df = pd.concat(tables, ignore_index=True)
        df.to_csv("docs/assets/output_table.csv")
    ```

=== "index.md"

    <code>
    My table:
    {{ read_csv("docs/assets/output_table.csv") }}
    </code>

=== "mkdocs.yml"

    ```yaml
    # ...
    plugins:
        - table-reader
    hooks:
        - scripts/hooks.py
    # ...
    ```

=== "Project structure"

    ```nohighlight
    .
    ├── scripts/
    │   └─── hooks.py
    ├── docs/
    │   └─── index.md
    │   └── assets/tables/
    │       └── table1.csv
    │       └── table2.csv
    └── mkdocs.yml
    ```

!!! note "Alternative: use jinja"

    You can also use jinja2 to display a list of tables. See how to [use jinja2 for automation](use_jinja2.md).

## Download a table from an API

=== "hooks.py"

    ```python
    import pandas as pd

    def on_pre_build(config, **kwargs) -> None:
        df = pd.read_csv('https://data.cityofnewyork.us/resource/nu7n-tubp.csv?$limit=100')
        df.to_csv("docs/assets/nyc_data.csv")
    ```

=== "index.md"

    <code>
    My table:
    {{ read_csv("docs/assets/nyc_data.csv") }}
    </code>

=== "mkdocs.yml"

    ```yaml
    # ...
    plugins:
        - table-reader
    hooks:
        - scripts/hooks.py
    # ...
    ```

=== "Project structure"

    ```nohighlight
    .
    ├── scripts/
    │   └─── hooks.py
    ├── docs/
    │   └─── index.md
    │   └── assets/
    └── mkdocs.yml
    ```

Note that during development when you use `mkdocs serve` and autoreload, you might not want to run this hook every time you make a change. You could use an environment variable inside your hook, for example something like `if os.environ['disable_hook'] == 1: return None`.

{% endraw %}
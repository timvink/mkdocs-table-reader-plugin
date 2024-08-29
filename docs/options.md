---
hide:
  - navigation
---

# Options
{% raw %}

You can customize the plugin by setting options in `mkdocs.yml`. For example:

```yml
plugins:
  - table-reader:
      data_path: "."
      allow_missing_files: False
      select_readers:
        - read_csv
        - read_json
      enabled: True
```

## `data_path`

Default is `.`. Set a default path to the searched directories in order to shorten table filename specifications.

Given a file path, `table-reader` will search for that file relative to your your project's `mkdocs.yml` and relative to your `docs/` folder. If you use a folder for all your table files you can shorten the path specification by setting the `data_path`.

For example, if your table is located in `docs/assets/tables/basic_table.csv`, you can set `data_path` to `docs/assets/tables/`. Then you will be able to use `{{ read_csv("basic_table.csv") }}` instead of `{{ read_csv("docs/assets/tables/basic_table.csv") }}` inside any markdown page.

!!! info

    Note that by default the plugin will _also_ search the page's directory but only when a table is not found.

    For more examples see the how to guide on [project structure](howto/project_structure.md).

## `allow_missing_files`

Default: `False`. When enabled, if a filepath is not found, the plugin will raise a warning instead of an error.

## `select_readers`

Default: Selects all available readers. Specify a list of readers to improve documentation build times for very large sites. This option is ignored when you use this plugin with `mkdocs-macros-plugin` ([read more](howto/use_jinja2.md))

## `enabled`

Default is `True`. Enables you to deactivate this plugin. This option is supported by all plugins since mkdocs 1.6 ([see docs](https://www.mkdocs.org/user-guide/configuration/#enabled-option)). A possible use case is local development where you might want faster build times and/or do not have the tables ready. It's recommended to use this option with an environment variable together with a default fallback (introduced in mkdocs v1.2.1, see docs). Example:

=== ":octicons-file-code-16: mkdocs.yml"

  ```yaml
  plugins:
    - table-reader:
        enabled: !ENV [ENABLED_TABLE_READER, True]
  ```

Which enables you to disable the plugin locally using:

```bash
export ENABLED_TABLE_READER=false
mkdocs serve
```

{% endraw %}
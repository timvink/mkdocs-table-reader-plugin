---
hide:
  - navigation
---

# Options

You can customize the plugin by setting options in `mkdocs.yml`. For example:

```yml
plugins:
  - table-reader:
      base_path: "config_dir"
      data_path: "."
      search_page_directory: True
```

#### `base_path`

The base path where `mkdocs-table-reader-plugin` will search for input files. The path to your table files should be relative to the `base_path`. Allowed values:

- `config_dir` (default): the directory where your project's `mkdocs.yml` file is located.
- `docs_dir`: the directory where your projects' `docs/` folder is located.

Note that by default the plugin will _also_ search the page's directory but only when a table is not found. 

#### `data_path`

The path to your table files should be relative to the `base_path`. If you use a folder for all your table files you can shorten the path specification by setting the `data_path`.

For example, if your table is located in `docs/tables/basic_table.csv`, you can set `data_path` to `docs/tables/` and `base_path` to `config_dir` (default). Then you will be able to use <code>\{\{ read_csv("basic_table.csv") \}\}</code> instead of <code>\{\{ read_csv("docs/tables/basic_table.csv") \}\}</code> inside any markdown page.

Default is `.`, which means you need to specify the path to your table files relative to the `base_path`.

Note that by default the plugin will _also_ search the page's directory but only when a table is not found.

#### `search_page_directory`

Default: `True`. When enabled, if a filepath is not found, the plugin will also attempt to find the file relative to the current page's directory. For example:

Note that even when True, the data path is searched first (i.e. relative to `data_path`),
and if a file is not found there, then the page's directory is searched. For example:

# Example

For example, consider the following project structure:

```nohighlight
.
├── docs/
│   ├── tables/
│   |   └── basic_table.csv
│   └── index.md
└── mkdocs.yml
```

In `index.md`, you can use:

- <code>\{\{ read_csv("docs/tables/basic_table.csv") \}\}</code> when `base_path` is set to `config_dir` (default)
- <code>\{\{ read_csv("tables/basic_table.csv") \}\}</code> when `base_path` is set to `docs_dir`
- <code>\{\{ read_csv("basic_table.csv") \}\}</code> when:
  - `search_page_directory` is enabled (default), OR
  - `bash_path` is set to `config_dir` and `data_path` is set to `docs/tables`, OR
  - `bash_path` is set to `docs_dir` and `data_path` is set to `tables`

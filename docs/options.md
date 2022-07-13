---
hide:
  - navigation
---

# Options

You can customize the plugin by setting options in `mkdocs.yml`. For example:

```yml
plugins:
  - table-reader:
      data_path: "docs"
      base_path: "config_dir"
```

#### `data_path`

Default is `.`, which means you can specify the path to your table files relative to the `base_path`, which defaults to the directory where your project's `mkdocs.yml` file is located. If you use a folder for all your table files you can shorten the path specification by setting `data_path`.

For example, if you set `data_path` to `docs/tables/` in the project below, you will be able to use <code>\{\{ read_csv("basic_table.csv") \}\}</code> instead of <code>\{\{ read_csv("docs/tables/basic_table.csv") \}\}</code> inside `index.md`.

```nohighlight
.
├── docs
│   ├── tables/
│   |   └── basic_table.csv
│   └── index.md
└── mkdocs.yml
```

#### `base_path`

The base path where `mkdocs-table-reader-plugin` will search for input files.
The value is a string, one of `docs_dir` or `config_dir`. The default is `config_dir`. 

- `config_dir`: the directory where your project's `mkdocs.yml` file is located.
- `docs_dir`: the directory where your projects' `docs/` folder is located.


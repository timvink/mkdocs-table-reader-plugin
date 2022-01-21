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
```

#### `data_path`

Default is `.`, which means you can specify the path to your table files relative to the location of your project's `mkdocs.yml` file. If you use a folder for all your table files you can shorten the path specification by setting `data_path`.

For example, if you set `data_path` to `docs/` in the project below, you will be able to use <code>\{\{ read_csv("basic_table.csv") \}\}</code> instead of <code>\{\{ read_csv("docs/basic_table.csv") \}\}</code> inside `index.md`.

```nohighlight
.
├── docs
│   ├── basic_table.csv
│   └── index.md
└── mkdocs.yml
```


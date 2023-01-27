# Choose a project structure

TODO.

- examples of different strategies/choices for storing tables?

## Example project structure

For example, consider the following project structure:

```nohighlight
.
├── docs/
│   ├── tables/
│   |   └── basic_table.csv
│   └── folder/
│       └── another_table.csv
│       └── page.md
└── mkdocs.yml
```

In `page.md`, to read `basic_table.csv`, you can use:

- <code>\{\{ read_csv("docs/tables/basic_table.csv") \}\}</code> when `base_path` is set to `config_dir` (default)
- <code>\{\{ read_csv("tables/basic_table.csv") \}\}</code> when `base_path` is set to `docs_dir`
- <code>\{\{ read_csv("basic_table.csv") \}\}</code> when:
    - `bash_path` is set to `config_dir` and `data_path` is set to `docs/tables`, OR
    - `bash_path` is set to `docs_dir` and `data_path` is set to `tables`

In `page.md`, to read `another_table.csv`, you can use:

- <code>\{\{ read_csv("docs/folder/another_table.csv") \}\}</code> when `base_path` is set to `config_dir` (default)
- <code>\{\{ read_csv("folder/another_table.csv") \}\}</code> when `base_path` is set to `docs_dir`
- <code>\{\{ read_csv("another_table.csv") \}\}</code> when:
    - `search_page_directory` is enabled (default), OR
    - `bash_path` is set to `config_dir` and `data_path` is set to `docs/folder`, OR
    - `bash_path` is set to `docs_dir` and `data_path` is set to `folder`

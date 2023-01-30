# Choose a project structure

You have different possible strategies to store and load your tables. This guide gives some examples.

## One table per markdown file

If you only want to include an occasional table in a specific markdown file, just store it in the same directory as the markdown file:

=== "project structure"

    ```nohighlight
    .
    ├── docs/
    │   ├── index.md
    │   └── folder/
    │       └── another_table.csv
    │       └── page.md
    └── mkdocs.yml
    ```

=== "folder/page.md"

    ```md
    Here is the table:

    \{\{ read_csv("another_table.csv") \}\}
    ```

This works because the [option](../options.md) `search_page_directory` defaults to `True`.

## Re-using tables across markdown files

If you want to re-use tables in multiple markdown files, you'll want to store them in a central directory, like `docs/assets/tables`. 
That way, if you restructure your navigation, the links to the tables won't break either.
It's also great if you generate tables because the output directory will be the same.

Given the following project structure:

```nohighlight
.
├── docs/
│   ├── index.md
│   └── folder/
│       └── page.md
│   └── assets/
│       └── tables/
│           └── another_table.csv
│           └── page.md
└── mkdocs.yml
```

In `page.md`, to read `basic_table.csv`, you can choose to use:

- <code>\{\{ read_csv("docs/assets/tables/another_table.csv") \}\}</code> when `base_path` [option](../options.md) is set to `config_dir` (default)
- <code>\{\{ read_csv("assets/tables/another_table.csv") \}\}</code> when `base_path` [option](../options.md) is set to `docs_dir`
- <code>\{\{ read_csv("../another_table.csv") \}\}</code> if you want to use a relative path and `search_page_directory` [option](../options.md) is enabled (default). Note that `..` stands for "one directory up".

## A central table directory combined with same-directory tables

If you have some central tables that you want to re-use, and some tables that are specific to a page, you could use the following project structure:

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

In `page.md`, to read `basic_table.csv`, you can choose to use:

- <code>\{\{ read_csv("docs/tables/basic_table.csv") \}\}</code> when `base_path` [option](../options.md) is set to `config_dir` (default)
- <code>\{\{ read_csv("tables/basic_table.csv") \}\}</code> when `base_path` [option](../options.md) is set to `docs_dir`
- <code>\{\{ read_csv("basic_table.csv") \}\}</code> when:
    - `bash_path` [option](../options.md) is set to `config_dir` and `data_path` is set to `docs/tables`, OR
    - `bash_path` [option](../options.md) is set to `docs_dir` and `data_path` is set to `tables`

In `page.md`, to read `another_table.csv`, you can choose to use:

- <code>\{\{ read_csv("docs/folder/another_table.csv") \}\}</code> when `base_path` is set to `config_dir` (default)
- <code>\{\{ read_csv("folder/another_table.csv") \}\}</code> when `base_path` is set to `docs_dir`
- <code>\{\{ read_csv("another_table.csv") \}\}</code> when:
    - `search_page_directory` [option](../options.md) is enabled (default), OR
    - `bash_path` [option](../options.md) is set to `config_dir` and `data_path` is set to `docs/folder`, OR
    - `bash_path` [option](../options.md) is set to `docs_dir` and `data_path` is set to `folder`

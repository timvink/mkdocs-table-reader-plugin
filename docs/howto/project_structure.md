# Choose a project structure
{% raw %}

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

    {{ read_csv("another_table.csv") }}
    ```

In `page.md`, to read `another_table.csv`, you can choose to use:

- `{{ read_csv("docs/folder/another_table.csv") }}` (Path relative to mkdocs.yml)
- `{{ read_csv("folder/another_table.csv") }}` (Path relative to docs/ directory)
- `{{ read_csv("another_table.csv") }}` (Path relative to page source file)

## Reusing tables across markdown files

If you want to reuse tables in multiple markdown files, or have many tables, you'll want to store them in a central directory, like `docs/assets/tables`. 
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
└── mkdocs.yml
```

In `page.md`, to read `another_table.csv`, you can choose to use:

- `{{ read_csv("docs/assets/tables/another_table.csv") }}` (Path relative to mkdocs.yml)
- `{{ read_csv("assets/tables/another_table.csv") }}` (Path relative to docs/ directory)
- `{{ read_csv("../assets/tables/another_table.csv") }}` (Path relative to page source file _(note that `..` stands for "one directory up")_)

{% endraw %}
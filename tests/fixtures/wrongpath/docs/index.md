# Test page

This is a table that we load from the docs folder, because we set `data_path` to `docs`:

## Missing table

{{ read_csv("non_existing_table.csv") }}

## Existing table

{{ read_csv("basic_table.csv") }}
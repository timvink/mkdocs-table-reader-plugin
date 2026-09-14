# Test page

Only `read_csv` is selected in mkdocs.yml.

## A selected reader

{{ read_csv("basic_table.csv") }}

## A reader that is not selected

{{ read_json("data.json") }}

# edge case

## a table with a carriage return

Discussed in issue [#2](https://github.com/timvink/mkdocs-table-reader-plugin/issues/2).

{{ read_table('assets/tables/table_with_carriage_return.csv', sep = ',') }}

## using `read_csv()`

{{ read_csv('assets/tables/table_with_carriage_return.csv') }}


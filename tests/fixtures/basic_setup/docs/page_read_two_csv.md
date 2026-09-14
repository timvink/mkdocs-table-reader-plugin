# two CSV

Discussed in [#4](https://github.com/timvink/mkdocs-table-reader-plugin/issues/4)

## table 1

The latest numbers using `read_table()`:

{{ read_table('assets/tables/basic_table.csv', sep = ',') }}

## table 2

{{ read_table('assets/tables/basic_table2.csv', sep = ',') }}

## Both on one line

Two tags on the same line are two tables: {{ read_csv('assets/tables/basic_table.csv') }} and {{ read_csv('assets/tables/basic_table2.csv') }} and that is that.

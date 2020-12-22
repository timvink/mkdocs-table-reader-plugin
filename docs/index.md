# table-reader plugin

This site serves as an example of how to use the [`table-reader`](https://github.com/timvink/mkdocs-table-reader-plugin) plugin.

## read_csv

The table below was inserted using the <code>\{\{ read_csv('tables/basic_table.csv') \}\}</code> tag:

{{ read_csv('tables/basic_table.csv') }}

## read_excel

The table below was inserted using the <code>\{\{ read_excel('tables/excel_table.xlsx') \}\}</code> tag:

{{ read_excel('tables/excel_table.xlsx') }}

## read_fwf

The table below was inserted using the <code>\{\{ read_fwf('tables/fixedwidth_table.txt') \}\}</code> tag:

{{ read_fwf('tables/fixedwidth_table.txt') }}

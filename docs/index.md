# table-reader plugin

This site serves as an example of how to use the [`table-reader`](https://github.com/timvink/mkdocs-table-reader-plugin) plugin.

## read_csv

The table below was inserted using the <code>\{\{ read_csv('tables/basic_table.csv') \}\}</code> tag:

{{ read_csv('tables/basic_table.csv') }}

## read_excel

The table below was inserted using the <code>\{\{ read_excel('tables/excel_table.xlsx') \}\}</code> tag:

{{ read_excel('tables/excel_table.xlsx') }}

!!! info "Reading xlsx files"

    You might get a `XLRDError('Excel xlsx file; not supported',)` error on linux systems. That's because `xlrd` does not support `.xlsx` files ([stackoverflow post](https://stackoverflow.com/questions/65254535/xlrd-biffh-xlrderror-excel-xlsx-file-not-supported)).
    Instead, install [openpyxl](https://openpyxl.readthedocs.io/en/stable/) and use:

    <code>\{\{ read_excel('tables/excel_table.xlsx', engine='openpyxl') \}\}</code>

## read_fwf

The table below was inserted using the <code>\{\{ read_fwf('tables/fixedwidth_table.txt') \}\}</code> tag:

{{ read_fwf('tables/fixedwidth_table.txt') }}

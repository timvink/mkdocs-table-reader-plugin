---
hide:
  - navigation
---

# Readers

The following table reader functions are available"

## read_csv

`{{ read_csv() }}` passed to [pandas.read_csv()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html). Example:

=== "Input"

    <code>\{\{ read_csv('tables/basic_table.csv') \}\}</code>

=== "Output"

    {{ read_csv('tables/basic_table.csv') }}


## read_fwf

`{{ read_fwf() }}` passed to [pandas.read_fwf()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_fwf.html). Example:

=== "Input"

    <code>\{\{ read_fwf('tables/fixedwidth_table.txt') \}\}</code>

=== "Output"

    {{ read_fwf('tables/fixedwidth_table.txt') }}


## read_yaml

`{{ read_yaml() }}` is parsed with [yaml.safe_load()](https://pyyaml.org/wiki/PyYAMLDocumentation#loading-yaml) and passed to [pandas.json_normalize()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.json_normalize.html). Example:

=== "Input"

    <code>\{\{ read_yaml('tables/yaml_table.yml') \}\}</code>

=== "Output"

    {{ read_yaml('tables/yaml_table.yml') }}


## read_table

`{{ read_table() }}` passed to [pandas.read_table()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_table.html). Example:

=== "Input"

    <code>\{\{ read_table('tables/basic_table.csv', sep = ',') \}\}</code>

=== "Output"

    {{ read_table('tables/basic_table.csv', sep = ',') }}


## read_excel

`{{ read_excel() }}` passed to [pandas.read_excel()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_excel.html). Example:


=== "Input"

    <code>\{\{ read_excel('tables/excel_table.xlsx') \}\}</code>

=== "Output"

    {{ read_excel('tables/excel_table.xlsx') }}


!!! info "Reading xlsx files"

    You might get a `XLRDError('Excel xlsx file; not supported',)` error when trying to read modern excel files. That's because `xlrd` does not support `.xlsx` files ([stackoverflow post](https://stackoverflow.com/questions/65254535/xlrd-biffh-xlrderror-excel-xlsx-file-not-supported)). Instead, install [openpyxl](https://openpyxl.readthedocs.io/en/stable/) and use:

    <code>\{\{ read_excel('tables/excel_table.xlsx', engine='openpyxl') \}\}</code>


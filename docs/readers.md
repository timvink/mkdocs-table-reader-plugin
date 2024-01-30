---
hide:
  - navigation
---

# Readers

The following table reader functions are available:

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

## read_json

`{{ read_json() }}` passed to [pandas.read_json()](https://pandas.pydata.org/docs/reference/api/pandas.read_json.html). Example:

=== "Input"

    <code>\{\{ read_json('tables/data.json', orient='split') \}\}</code>

=== "Output"

    {{ read_json('tables/data.json', orient='split') }}

## read_feather

`{{ read_feather() }}` passed to [pandas.read_feather()](https://pandas.pydata.org/docs/reference/api/pandas.read_feather.html). Example:

=== "Input"

    <code>\{\{ read_json('tables/data.feather') \}\}</code>

=== "Output"

    {{ read_feather('tables/data.feather') }}


## read_excel

`{{ read_excel() }}` passed to [pandas.read_excel()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_excel.html). Example:


=== "Input"

    <code>\{\{ read_excel('tables/excel_table.xlsx', engine='openpyxl') \}\}</code>

=== "Output"

    {{ read_excel('tables/excel_table.xlsx', engine='openpyxl') }}


!!! info "Reading xlsx files"

    You might get a `XLRDError('Excel xlsx file; not supported',)` error when trying to read modern excel files. That's because `xlrd` does not support `.xlsx` files ([stackoverflow post](https://stackoverflow.com/questions/65254535/xlrd-biffh-xlrderror-excel-xlsx-file-not-supported)). Instead, install [openpyxl](https://openpyxl.readthedocs.io/en/stable/) and use:

    <code>\{\{ read_excel('tables/excel_table.xlsx', engine='openpyxl') \}\}</code>

## read_raw

`{{ read_raw() }}` inserts contents from a file directly. This is great if you have a file with a table already in markdown format. 
It could also replace a workflow where you use the [snippets extension to embed external files](https://squidfunk.github.io/mkdocs-material/reference/code-blocks/#embedding-external-files).

Example:

=== "Input"

    <code>\{\{ read_raw('tables/markdown_table.md') \}\}</code>

=== "Output"

    {{ read_raw('tables/markdown_table.md') }}


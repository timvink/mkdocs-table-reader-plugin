---
hide:
  - navigation
---

# Readers

The following table reader functions are available:

## read_csv

{% raw %}`{{ read_csv() }}`{% endraw %} passed to [pandas.read_csv()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html). Example:

=== "Input"

    {% raw %}
    ```markdown
    {{ read_csv('assets/tables/basic_table.csv') }}`
    ```
    {% endraw %}

=== "Output"

    {{ read_csv('assets/tables/basic_table.csv') | add_indentation(spaces=4) }}


## read_fwf

{% raw %}`{{ read_fwf() }}`{% endraw %} passed to [pandas.read_fwf()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_fwf.html). Example:

=== "Input"

    {% raw %}
    ```markdown
    {{ read_fwf('assets/tables/fixedwidth_table.txt') }}
    ```
    {% endraw %}

=== "Output"

    {{ read_fwf('assets/tables/fixedwidth_table.txt') | add_indentation(spaces=4) }}


## read_yaml

{% raw %}`{{ read_yaml() }}`{% endraw %} is parsed with [yaml.safe_load()](https://pyyaml.org/wiki/PyYAMLDocumentation#loading-yaml) and passed to [pandas.json_normalize()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.json_normalize.html). Example:

=== "Input"

    {% raw %}
    ```markdown
    {{ read_yaml('assets/tables/yaml_table.yml') }}
    ```
    {% endraw %}

=== "Output"

    {{ read_yaml('assets/tables/yaml_table.yml') | add_indentation(spaces=4) }}


## read_table

{% raw %}`{{ read_table() }}`{% endraw %} passed to [pandas.read_table()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_table.html). Example:

=== "Input"

    {% raw %}
    ```markdown
    {{ read_table('assets/tables/basic_table.csv', sep = ',') }}
    ```
    {% endraw %}

=== "Output"

    {{ read_table('assets/tables/basic_table.csv', sep = ',') | add_indentation(spaces=4) }}

## read_json

{% raw %}`{{ read_json() }}`{% endraw %} passed to [pandas.read_json()](https://pandas.pydata.org/docs/reference/api/pandas.read_json.html). Example:

=== "Input"

    {% raw %}
    ```markdown
    {{ read_json('assets/tables/data.json', orient='split') }}
    ```
    {% endraw %}

=== "Output"

    {{ read_json('assets/tables/data.json', orient='split') | add_indentation(spaces=4) }}

## read_feather

{% raw %}`{{ read_feather() }}`{% endraw %} passed to [pandas.read_feather()](https://pandas.pydata.org/docs/reference/api/pandas.read_feather.html). Example:

=== "Input"

    {% raw %}
    ```markdown
    {{ read_json('assets/tables/data.feather') }}
    ```
    {% endraw %}

=== "Output"

    {{ read_feather('assets/tables/data.feather')  | add_indentation(spaces=4) }}


## read_excel

{% raw %}`{{ read_excel() }}`{% endraw %} passed to [pandas.read_excel()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_excel.html). Example:


=== "Input"

    {% raw %}
    ```markdown
    {{ read_excel('assets/tables/excel_table.xlsx', engine='openpyxl') }}
    ```
    {% endraw %}

=== "Output"

    {{ read_excel('assets/tables/excel_table.xlsx', engine='openpyxl') | add_indentation(spaces=4) }}


!!! info "Reading xlsx files"

    You might get a `XLRDError('Excel xlsx file; not supported',)` error when trying to read modern excel files. That's because `xlrd` does not support `.xlsx` files ([stackoverflow post](https://stackoverflow.com/questions/65254535/xlrd-biffh-xlrderror-excel-xlsx-file-not-supported)). Instead, install [openpyxl](https://openpyxl.readthedocs.io/en/stable/) and use:

    {% raw %}
    ```markdown
    {{ read_excel('assets/tables/excel_table.xlsx', engine='openpyxl') }}
    ```
    {% endraw %}

## read_raw

{% raw %}`{{ read_raw() }}`{% endraw %} inserts contents from a file directly. This is great if you have a file with a table already in markdown format. 
It could also replace a workflow where you use the [snippets extension to embed external files](https://squidfunk.github.io/mkdocs-material/reference/code-blocks/#embedding-external-files).

Example:

=== "Input"

    {% raw %}
    ```markdown
    {{ read_raw('assets/tables/markdown_table.md') }}
    ```
    {% endraw %}

=== "Output"

    {{ read_raw('assets/tables/markdown_table.md')  | add_indentation(spaces=4) }}


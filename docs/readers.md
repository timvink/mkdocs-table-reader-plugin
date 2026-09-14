---
hide:
  - navigation
---

# Readers

## Basic readers

The following table reader functions are available:

### `read_csv`

Use {% raw %}`{{ read_csv() }}`{% endraw %} to read a comma-separated values (csv) and output as a markdown table.

1. Arguments are parsed safely and then passed to corresponding functions below
2. File is read using [pandas.read_csv()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html)
3. The `pd.DataFrame` is then converted to a markdown table using [`.to_markdown()`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_markdown.html)
4. The markdown table is fixed to match the indentation used by the tag in the markdown document (only when _not_ used with `mkdocs-macros-plugin`. See [compatibility with macros plugin](howto/use_jinja2.md))

Example:

=== "Input"

    {% raw %}
    ```markdown
    {{ read_csv('assets/tables/basic_table.csv') }}
    ```
    {% endraw %}

=== "Output"

    {{ read_csv('assets/tables/basic_table.csv') | add_indentation(spaces=4) }}

!!! info "Multiline cells"

    A markdown table row has to fit on a single line, so newlines inside a cell are
    replaced with `<br>`. Note that such a cell needs to be quoted to be valid CSV:

    ```csv
    id,description
    23456,"Some description.

    With a line break."
    ```


### `read_fwf`

Use {% raw %}`{{ read_fwf() }}`{% endraw %} to read a table of fixed-width formatted lines and output as a markdown table.

1. Arguments are parsed safely and then passed to corresponding functions below
2. File is read using [pandas.read_fwf()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_fwf.html)
3. The `pd.DataFrame` is then converted to a markdown table using [`.to_markdown()`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_markdown.html)
4. The markdown table is fixed to match the indentation used by the tag in the markdown document (only when _not_ used with `mkdocs-macros-plugin`. See [compatibility with macros plugin](howto/use_jinja2.md))

Example:

=== "Input"

    {% raw %}
    ```markdown
    {{ read_fwf('assets/tables/fixedwidth_table.txt') }}
    ```
    {% endraw %}

=== "Output"

    {{ read_fwf('assets/tables/fixedwidth_table.txt') | add_indentation(spaces=4) }}


### `read_yaml`

Use {% raw %}`{{ read_yaml() }}`{% endraw %} to read a YAML file and output as a markdown table.

1. Arguments are parsed safely and then passed to corresponding functions below
2. File is read using [yaml.safe_load()](https://pyyaml.org/wiki/PyYAMLDocumentation#loading-yaml) and then passed to [pandas.json_normalize()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.json_normalize.html)
3. The `pd.DataFrame` is then converted to a markdown table using [`.to_markdown()`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_markdown.html)
4. The markdown table is fixed to match the indentation used by the tag in the markdown document (only when _not_ used with `mkdocs-macros-plugin`. See [compatibility with macros plugin](howto/use_jinja2.md))

Example:

=== "Input"

    {% raw %}
    ```markdown
    {{ read_yaml('assets/tables/yaml_table.yml') }}
    ```
    {% endraw %}

=== "Output"

    {{ read_yaml('assets/tables/yaml_table.yml') | add_indentation(spaces=4) }}

The file is read as UTF-8. Use the `encoding` argument for files in another encoding, for example {% raw %}`{{ read_yaml('assets/tables/yaml_table.yml', encoding='cp1251') }}`{% endraw %}.


### `read_table`

Use {% raw %}`{{ read_table() }}`{% endraw %} to read a general delimited file and output as a markdown table.

1. Arguments are parsed safely and then passed to corresponding functions below
2. File is read using [pandas.read_table()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_table.html)
3. The `pd.DataFrame` is then converted to a markdown table using [`.to_markdown()`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_markdown.html)
4. The markdown table is fixed to match the indentation used by the tag in the markdown document (only when _not_ used with `mkdocs-macros-plugin`. See [compatibility with macros plugin](howto/use_jinja2.md))

Example:

=== "Input"

    {% raw %}
    ```markdown
    {{ read_table('assets/tables/basic_table.csv', sep = ',') }}
    ```
    {% endraw %}

=== "Output"

    {{ read_table('assets/tables/basic_table.csv', sep = ',') | add_indentation(spaces=4) }}

### `read_json`

Use {% raw %}`{{ read_json() }}`{% endraw %} to read a JSON string path and output as a markdown table.

1. Arguments are parsed safely and then passed to corresponding functions below
2. File is read using [pandas.read_json()](https://pandas.pydata.org/docs/reference/api/pandas.read_json.html)
3. The `pd.DataFrame` is then converted to a markdown table using [`.to_markdown()`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_markdown.html)
4. The markdown table is fixed to match the indentation used by the tag in the markdown document (only when _not_ used with `mkdocs-macros-plugin`. See [compatibility with macros plugin](howto/use_jinja2.md))

Example:

=== "Input"

    {% raw %}
    ```markdown
    {{ read_json('assets/tables/data.json', orient='split') }}
    ```
    {% endraw %}

=== "Output"

    {{ read_json('assets/tables/data.json', orient='split') | add_indentation(spaces=4) }}

### `read_feather`

Use {% raw %}`{{ read_feather() }}`{% endraw %} to read a feather-format object and output as a markdown table.

1. Arguments are parsed safely and then passed to corresponding functions below
2. File is read using [pandas.read_feather()](https://pandas.pydata.org/docs/reference/api/pandas.read_feather.html)
3. The `pd.DataFrame` is then converted to a markdown table using [`.to_markdown()`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_markdown.html)
4. The markdown table is fixed to match the indentation used by the tag in the markdown document (only when _not_ used with `mkdocs-macros-plugin`. See [compatibility with macros plugin](howto/use_jinja2.md))

Example:

=== "Input"

    {% raw %}
    ```markdown
    {{ read_feather('assets/tables/data.feather') }}
    ```
    {% endraw %}

=== "Output"

    {{ read_feather('assets/tables/data.feather')  | add_indentation(spaces=4) }}


### `read_excel`

Use {% raw %}`{{ read_excel() }}`{% endraw %} to read an Excel file and output as a markdown table.

1. Arguments are parsed safely and then passed to corresponding functions below
2. File is read using [pandas.read_excel()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_excel.html)
3. The `pd.DataFrame` is then converted to a markdown table using [`.to_markdown()`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_markdown.html)
4. The markdown table is fixed to match the indentation used by the tag in the markdown document (only when _not_ used with `mkdocs-macros-plugin`. See [compatibility with macros plugin](howto/use_jinja2.md))

Example:

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

### `read_parquet`

Use {% raw %}`{{ read_parquet() }}`{% endraw %} to read a parquet file and output as a markdown table.

1. Arguments are parsed safely and then passed to corresponding functions below
2. File is read using [pandas.read_parquet()](https://pandas.pydata.org/docs/reference/api/pandas.read_parquet.html)
3. The `pd.DataFrame` is then converted to a markdown table using [`.to_markdown()`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_markdown.html)
4. The markdown table is fixed to match the indentation used by the tag in the markdown document (only when _not_ used with `mkdocs-macros-plugin`. See [compatibility with macros plugin](howto/use_jinja2.md))

Example:

=== "Input"

    {% raw %}
    ```markdown
    {{ read_parquet('assets/tables/data.parquet') }}
    ```
    {% endraw %}

=== "Output"

    {{ read_parquet('assets/tables/data.parquet') | add_indentation(spaces=4) }}

Requires [pyarrow](https://arrow.apache.org/docs/python/install.html) or [fastparquet](https://fastparquet.readthedocs.io/en/latest/install.html) to be installed.

### `read_orc`

Use {% raw %}`{{ read_orc() }}`{% endraw %} to read an ORC object and output as a markdown table.

1. Arguments are parsed safely and then passed to corresponding functions below
2. File is read using [pandas.read_orc()](https://pandas.pydata.org/docs/reference/api/pandas.read_orc.html)
3. The `pd.DataFrame` is then converted to a markdown table using [`.to_markdown()`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_markdown.html)
4. The markdown table is fixed to match the indentation used by the tag in the markdown document (only when _not_ used with `mkdocs-macros-plugin`. See [compatibility with macros plugin](howto/use_jinja2.md))

Example:

=== "Input"

    {% raw %}
    ```markdown
    {{ read_orc('assets/tables/data.orc') }}
    ```
    {% endraw %}

=== "Output"

    {{ read_orc('assets/tables/data.orc') | add_indentation(spaces=4) }}

Requires [pyarrow](https://arrow.apache.org/docs/python/install.html) to be installed. On windows, `pandas.read_orc()` also needs the [IANA time zone database](https://arrow.apache.org/docs/python/timestamps.html) to be available to pyarrow.

### `read_xml`

Use {% raw %}`{{ read_xml() }}`{% endraw %} to read an XML document and output as a markdown table.

1. Arguments are parsed safely and then passed to corresponding functions below
2. File is read using [pandas.read_xml()](https://pandas.pydata.org/docs/reference/api/pandas.read_xml.html)
3. The `pd.DataFrame` is then converted to a markdown table using [`.to_markdown()`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_markdown.html)
4. The markdown table is fixed to match the indentation used by the tag in the markdown document (only when _not_ used with `mkdocs-macros-plugin`. See [compatibility with macros plugin](howto/use_jinja2.md))

Example:

=== "Input"

    {% raw %}
    ```markdown
    {{ read_xml('assets/tables/data.xml') }}
    ```
    {% endraw %}

=== "Output"

    {{ read_xml('assets/tables/data.xml') | add_indentation(spaces=4) }}

Requires [lxml](https://lxml.de/installation.html) to be installed, or use the standard library parser with {% raw %}`{{ read_xml('assets/tables/data.xml', parser='etree') }}`{% endraw %}.

### `read_html`

Use {% raw %}`{{ read_html() }}`{% endraw %} to read the first table in an HTML document and output as a markdown table.

1. Arguments are parsed safely and then passed to corresponding functions below
2. File is read using [pandas.read_html()](https://pandas.pydata.org/docs/reference/api/pandas.read_html.html)
3. The `pd.DataFrame` is then converted to a markdown table using [`.to_markdown()`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_markdown.html)
4. The markdown table is fixed to match the indentation used by the tag in the markdown document (only when _not_ used with `mkdocs-macros-plugin`. See [compatibility with macros plugin](howto/use_jinja2.md))

Example:

=== "Input"

    {% raw %}
    ```markdown
    {{ read_html('assets/tables/data.html') }}
    ```
    {% endraw %}

=== "Output"

    {{ read_html('assets/tables/data.html') | add_indentation(spaces=4) }}

`pandas.read_html()` returns every table it finds, so the first one is inserted. Use the `match` argument to select another table, for example {% raw %}`{{ read_html('assets/tables/data.html', match='price') }}`{% endraw %}. Requires [lxml](https://lxml.de/installation.html), or [beautifulsoup4](https://pypi.org/project/beautifulsoup4/) and [html5lib](https://pypi.org/project/html5lib/), to be installed.

### `read_stata`

Use {% raw %}`{{ read_stata() }}`{% endraw %} to read a Stata file and output as a markdown table.

1. Arguments are parsed safely and then passed to corresponding functions below
2. File is read using [pandas.read_stata()](https://pandas.pydata.org/docs/reference/api/pandas.read_stata.html)
3. The `pd.DataFrame` is then converted to a markdown table using [`.to_markdown()`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_markdown.html)
4. The markdown table is fixed to match the indentation used by the tag in the markdown document (only when _not_ used with `mkdocs-macros-plugin`. See [compatibility with macros plugin](howto/use_jinja2.md))

Example:

=== "Input"

    {% raw %}
    ```markdown
    {{ read_stata('assets/tables/data.dta') }}
    ```
    {% endraw %}

=== "Output"

    {{ read_stata('assets/tables/data.dta') | add_indentation(spaces=4) }}

### `read_sas`

Use {% raw %}`{{ read_sas() }}`{% endraw %} to read a SAS file (XPORT or SAS7BDAT) and output as a markdown table.

1. Arguments are parsed safely and then passed to corresponding functions below
2. File is read using [pandas.read_sas()](https://pandas.pydata.org/docs/reference/api/pandas.read_sas.html)
3. The `pd.DataFrame` is then converted to a markdown table using [`.to_markdown()`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_markdown.html)
4. The markdown table is fixed to match the indentation used by the tag in the markdown document (only when _not_ used with `mkdocs-macros-plugin`. See [compatibility with macros plugin](howto/use_jinja2.md))

Example:

=== "Input"

    {% raw %}
    ```markdown
    {{ read_sas('assets/tables/data.xpt', encoding='utf-8') }}
    ```
    {% endraw %}

=== "Output"

    {{ read_sas('assets/tables/data.xpt', encoding='utf-8') | add_indentation(spaces=4) }}

Text columns are read as bytes unless you specify the `encoding` to decode them with.

### `read_spss`

Use {% raw %}`{{ read_spss() }}`{% endraw %} to read an SPSS file and output as a markdown table.

1. Arguments are parsed safely and then passed to corresponding functions below
2. File is read using [pandas.read_spss()](https://pandas.pydata.org/docs/reference/api/pandas.read_spss.html)
3. The `pd.DataFrame` is then converted to a markdown table using [`.to_markdown()`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_markdown.html)
4. The markdown table is fixed to match the indentation used by the tag in the markdown document (only when _not_ used with `mkdocs-macros-plugin`. See [compatibility with macros plugin](howto/use_jinja2.md))

Example:

{% raw %}
```markdown
{{ read_spss('assets/tables/data.sav') }}
```
{% endraw %}

Requires [pyreadstat](https://github.com/Roche/pyreadstat) to be installed.

### `read_hdf`

Use {% raw %}`{{ read_hdf() }}`{% endraw %} to read an object stored in a HDF5 file and output as a markdown table.

1. Arguments are parsed safely and then passed to corresponding functions below
2. File is read using [pandas.read_hdf()](https://pandas.pydata.org/docs/reference/api/pandas.read_hdf.html)
3. The `pd.DataFrame` is then converted to a markdown table using [`.to_markdown()`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_markdown.html)
4. The markdown table is fixed to match the indentation used by the tag in the markdown document (only when _not_ used with `mkdocs-macros-plugin`. See [compatibility with macros plugin](howto/use_jinja2.md))

Example:

{% raw %}
```markdown
{{ read_hdf('assets/tables/data.h5', key='table') }}
```
{% endraw %}

Requires [pytables](https://www.pytables.org/usersguide/installation.html) to be installed. Specify the `key` of the object to read when the file contains more than one.

### `read_raw`

Use {% raw %}`{{ read_raw() }}`{% endraw %} to insert the contents from a file directly. 

This is great if you have a file with a table already in markdown format. 
It could also replace a workflow where you use the [snippets extension to embed external files](https://squidfunk.github.io/mkdocs-material/reference/code-blocks/#embedding-external-files).

1. Only the first argument is read. This should be the file path.
2. File is read using python
4. The markdown table is fixed to match the indentation used by the tag in the markdown document (only when _not_ used with `mkdocs-macros-plugin`. See [compatibility with macros plugin](howto/use_jinja2.md))

Example:

=== "Input"

    {% raw %}
    ```markdown
    {{ read_raw('assets/tables/markdown_table.md') }}
    ```
    {% endraw %}

=== "Output"

    {{ read_raw('assets/tables/markdown_table.md')  | add_indentation(spaces=4) }}

The file is read as UTF-8. Use the `encoding` argument for files in another encoding, for example {% raw %}`{{ read_raw('assets/tables/markdown_table.md', encoding='cp1251') }}`{% endraw %}.


## Macros

When you use `table-reader` with [`mkdocs-macros-plugin`](https://mkdocs-macros-plugin.readthedocs.io/en/latest/), in next to all the readers, the following _additional_ macros will be made available:

### `pd_read_csv`

Use {% raw %}`{{ pd_read_csv() }}`{% endraw %} to read a comma-separated values (csv) using [pandas.read_csv()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html).

=== "Input"

    {% raw %}
    ```markdown
    {{ pd_read_csv('assets/tables/basic_table.csv').to_markdown(tablefmt="pipe", index=False) | add_indentation(spaces=4) }}
    ```
    {% endraw %}

=== "Output"

    {{ pd_read_csv('assets/tables/basic_table.csv').to_markdown(tablefmt="pipe", index=False) | add_indentation(spaces=4) }}


### `pd_read_fwf`

Use {% raw %}`{{ pd_read_fwf() }}`{% endraw %} to read a table of fixed-width formatted lines using [pandas.read_fwf()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_fwf.html)

Example:

=== "Input"

    {% raw %}
    ```markdown
    {{ pd_read_fwf('assets/tables/fixedwidth_table.txt').to_markdown(tablefmt="pipe", index=False) | add_indentation(spaces=4) }}
    ```
    {% endraw %}

=== "Output"

    {{ pd_read_fwf('assets/tables/fixedwidth_table.txt').to_markdown(tablefmt="pipe", index=False) | add_indentation(spaces=4) }}


### `pd_read_yaml`

Use {% raw %}`{{ pd_read_yaml() }}`{% endraw %} to read a YAML file using [yaml.safe_load()](https://pyyaml.org/wiki/PyYAMLDocumentation#loading-yaml) and [pandas.json_normalize()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.json_normalize.html).

Example:

=== "Input"

    {% raw %}
    ```markdown
    {{ pd_read_yaml('assets/tables/yaml_table.yml').to_markdown(tablefmt="pipe", index=False) | add_indentation(spaces=4) }}
    ```
    {% endraw %}

=== "Output"

    {{ pd_read_yaml('assets/tables/yaml_table.yml').to_markdown(tablefmt="pipe", index=False) | add_indentation(spaces=4) }}

The file is read as UTF-8. Use the `encoding` argument for files in another encoding, for example {% raw %}`{{ pd_read_yaml('assets/tables/yaml_table.yml', encoding='cp1251') }}`{% endraw %}.


### `pd_read_table`

Use {% raw %}`{{ pd_read_table() }}`{% endraw %} to read a general delimited file using [pandas.read_table()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_table.html).

Example:

=== "Input"

    {% raw %}
    ```markdown
    {{ pd_read_table('assets/tables/basic_table.csv', sep = ',').to_markdown(tablefmt="pipe", index=False) | add_indentation(spaces=4) }}
    ```
    {% endraw %}

=== "Output"

    {{ pd_read_table('assets/tables/basic_table.csv', sep = ',').to_markdown(tablefmt="pipe", index=False) | add_indentation(spaces=4) }}



### `pd_read_json`

Use {% raw %}`{{ pd_read_json() }}`{% endraw %} to read a JSON string path using [pandas.read_json()](https://pandas.pydata.org/docs/reference/api/pandas.read_json.html)

Example:

=== "Input"

    {% raw %}
    ```markdown
    {{ pd_read_json('assets/tables/data.json', orient='split').to_markdown(tablefmt="pipe", index=False) | add_indentation(spaces=4) }}
    ```
    {% endraw %}

=== "Output"

    {{ pd_read_json('assets/tables/data.json', orient='split').to_markdown(tablefmt="pipe", index=False) | add_indentation(spaces=4) }}



### `pd_read_feather`

Use {% raw %}`{{ pd_read_feather() }}`{% endraw %} to read a feather-format object using [pandas.read_feather()](https://pandas.pydata.org/docs/reference/api/pandas.read_feather.html)


Example:

=== "Input"

    {% raw %}
    ```markdown
    {{ pd_read_feather('assets/tables/data.feather').to_markdown(tablefmt="pipe", index=False) | add_indentation(spaces=4) }}
    ```
    {% endraw %}

=== "Output"

    {{ pd_read_feather('assets/tables/data.feather').to_markdown(tablefmt="pipe", index=False) | add_indentation(spaces=4) }}


### `pd_read_excel`

Use {% raw %}`{{ pd_read_excel() }}`{% endraw %} to read an Excel file using [pandas.read_excel()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_excel.html)

Example:

=== "Input"

    {% raw %}
    ```markdown
    {{ pd_read_excel('assets/tables/excel_table.xlsx', engine='openpyxl').to_markdown(tablefmt="pipe", index=False) | add_indentation(spaces=4) }}
    ```
    {% endraw %}

=== "Output"

    {{ pd_read_excel('assets/tables/excel_table.xlsx', engine='openpyxl').to_markdown(tablefmt="pipe", index=False) | add_indentation(spaces=4) }}


!!! info "Reading xlsx files"

    You might get a `XLRDError('Excel xlsx file; not supported',)` error when trying to read modern excel files. That's because `xlrd` does not support `.xlsx` files ([stackoverflow post](https://stackoverflow.com/questions/65254535/xlrd-biffh-xlrderror-excel-xlsx-file-not-supported)). Instead, install [openpyxl](https://openpyxl.readthedocs.io/en/stable/) and use:

    {% raw %}
    ```markdown
    {{ pd_read_excel('assets/tables/excel_table.xlsx', engine='openpyxl') }}
    ```
    {% endraw %}


### `pd_read_parquet`

Use {% raw %}`{{ pd_read_parquet() }}`{% endraw %} to read a parquet file using [pandas.read_parquet()](https://pandas.pydata.org/docs/reference/api/pandas.read_parquet.html)

Example:

=== "Input"

    {% raw %}
    ```markdown
    {{ pd_read_parquet('assets/tables/data.parquet').to_markdown(tablefmt="pipe", index=False) | add_indentation(spaces=4) }}
    ```
    {% endraw %}

=== "Output"

    {{ pd_read_parquet('assets/tables/data.parquet').to_markdown(tablefmt="pipe", index=False) | add_indentation(spaces=4) }}

### `pd_read_orc`

Use {% raw %}`{{ pd_read_orc() }}`{% endraw %} to read an ORC object using [pandas.read_orc()](https://pandas.pydata.org/docs/reference/api/pandas.read_orc.html)

Example:

=== "Input"

    {% raw %}
    ```markdown
    {{ pd_read_orc('assets/tables/data.orc').to_markdown(tablefmt="pipe", index=False) | add_indentation(spaces=4) }}
    ```
    {% endraw %}

=== "Output"

    {{ pd_read_orc('assets/tables/data.orc').to_markdown(tablefmt="pipe", index=False) | add_indentation(spaces=4) }}

### `pd_read_xml`

Use {% raw %}`{{ pd_read_xml() }}`{% endraw %} to read an XML document using [pandas.read_xml()](https://pandas.pydata.org/docs/reference/api/pandas.read_xml.html)

Example:

=== "Input"

    {% raw %}
    ```markdown
    {{ pd_read_xml('assets/tables/data.xml').to_markdown(tablefmt="pipe", index=False) | add_indentation(spaces=4) }}
    ```
    {% endraw %}

=== "Output"

    {{ pd_read_xml('assets/tables/data.xml').to_markdown(tablefmt="pipe", index=False) | add_indentation(spaces=4) }}

### `pd_read_html`

Use {% raw %}`{{ pd_read_html() }}`{% endraw %} to read the first table in an HTML document using [pandas.read_html()](https://pandas.pydata.org/docs/reference/api/pandas.read_html.html)

Example:

=== "Input"

    {% raw %}
    ```markdown
    {{ pd_read_html('assets/tables/data.html').to_markdown(tablefmt="pipe", index=False) | add_indentation(spaces=4) }}
    ```
    {% endraw %}

=== "Output"

    {{ pd_read_html('assets/tables/data.html').to_markdown(tablefmt="pipe", index=False) | add_indentation(spaces=4) }}

### `pd_read_stata`

Use {% raw %}`{{ pd_read_stata() }}`{% endraw %} to read a Stata file using [pandas.read_stata()](https://pandas.pydata.org/docs/reference/api/pandas.read_stata.html)

Example:

=== "Input"

    {% raw %}
    ```markdown
    {{ pd_read_stata('assets/tables/data.dta').to_markdown(tablefmt="pipe", index=False) | add_indentation(spaces=4) }}
    ```
    {% endraw %}

=== "Output"

    {{ pd_read_stata('assets/tables/data.dta').to_markdown(tablefmt="pipe", index=False) | add_indentation(spaces=4) }}

### `pd_read_sas`

Use {% raw %}`{{ pd_read_sas() }}`{% endraw %} to read a SAS file (XPORT or SAS7BDAT) using [pandas.read_sas()](https://pandas.pydata.org/docs/reference/api/pandas.read_sas.html)

Example:

=== "Input"

    {% raw %}
    ```markdown
    {{ pd_read_sas('assets/tables/data.xpt', encoding='utf-8').to_markdown(tablefmt="pipe", index=False) | add_indentation(spaces=4) }}
    ```
    {% endraw %}

=== "Output"

    {{ pd_read_sas('assets/tables/data.xpt', encoding='utf-8').to_markdown(tablefmt="pipe", index=False) | add_indentation(spaces=4) }}

### `pd_read_spss`

Use {% raw %}`{{ pd_read_spss() }}`{% endraw %} to read an SPSS file using [pandas.read_spss()](https://pandas.pydata.org/docs/reference/api/pandas.read_spss.html)

Example:

{% raw %}
```markdown
{{ pd_read_spss('assets/tables/data.sav').to_markdown(tablefmt="pipe", index=False) | add_indentation(spaces=4) }}
```
{% endraw %}

### `pd_read_hdf`

Use {% raw %}`{{ pd_read_hdf() }}`{% endraw %} to read an object stored in a HDF5 file using [pandas.read_hdf()](https://pandas.pydata.org/docs/reference/api/pandas.read_hdf.html)

Example:

{% raw %}
```markdown
{{ pd_read_hdf('assets/tables/data.h5', key='table').to_markdown(tablefmt="pipe", index=False) | add_indentation(spaces=4) }}
```
{% endraw %}

## Filters

When you use `table-reader` with [`mkdocs-macros-plugin`](https://mkdocs-macros-plugin.readthedocs.io/en/latest/), in next to all the readers, the macros, the following _additional_ filters will be made available:

### `add_indentation`

Adds a consistent indentation to every line in a string. This is important when you are inserting content into [Admonitions](https://squidfunk.github.io/mkdocs-material/reference/admonitions/) or [Content tabs](https://squidfunk.github.io/mkdocs-material/reference/content-tabs/).

Args:
    text (str): input text
    spaces (int): Indentation to add in spaces
    tabs (int): Indentation to add in tabs


Example usage: 

{% raw %}
```markdown
!!! note "this is a note"
    {{ pd_read_csv('assets/tables/basic_table.csv').to_markdown(tablefmt="pipe", index=False) | add_indentation(spaces=4) }}
```
{% endraw %}

### `convert_to_md_table`

Converts a pandas dataframe into a markdown table. Arguments are passed to [`.to_markdown()`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_markdown.html). By default, `tablefmt='pipe'` and `index=False` are used.
There is also an additional fix to ensure any pipe (`|`) characters in the dataframe are properly escaped ([python-tabulate#241](https://github.com/astanin/python-tabulate/issues/241)).

Example usage: 

{% raw %}
```markdown
{{ pd_read_csv('assets/tables/basic_table.csv') | convert_to_md_table  }}
```
{% endraw %}


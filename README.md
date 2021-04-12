[![Actions Status](https://github.com/timvink/mkdocs-table-reader-plugin/workflows/pytest/badge.svg)](https://github.com/timvink/mkdocs-table-reader-plugin/actions)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mkdocs-table-reader-plugin)
![PyPI](https://img.shields.io/pypi/v/mkdocs-table-reader-plugin)
![PyPI - Downloads](https://img.shields.io/pypi/dm/mkdocs-table-reader-plugin)
[![codecov](https://codecov.io/gh/timvink/mkdocs-table-reader-plugin/branch/master/graph/badge.svg)](https://codecov.io/gh/timvink/mkdocs-table-reader-plugin)
![GitHub contributors](https://img.shields.io/github/contributors/timvink/mkdocs-table-reader-plugin)
![PyPI - License](https://img.shields.io/pypi/l/mkdocs-table-reader-plugin)

# mkdocs-table-reader-plugin

[MkDocs](https://www.mkdocs.org/) plugin that adds a `{{ read_csv('table.csv') }}` markdown tag to directly insert CSV files as a table into a page. See it in action at [timvink.github.io/mkdocs-table-reader-plugin/](https://timvink.github.io/mkdocs-table-reader-plugin/).

This makes it easier to build reproducible reports. For more complex use cases, consider [mknotebooks](https://github.com/greenape/mknotebooks), [mkdocs-markdownextradata-plugin](https://github.com/rosscdh/mkdocs-markdownextradata-plugin) or [mkdocs-macros-plugin](https://mkdocs-macros-plugin.readthedocs.io/en/latest/).

## Setup

Install the plugin using `pip3`:

```bash
pip3 install mkdocs-table-reader-plugin
```

Next, add the following lines to your `mkdocs.yml`:

```yml
plugins:
  - search
  - table-reader
```

> If you have no `plugins` entry in your config file yet, you'll likely also want to add the `search` plugin. MkDocs enables it by default if there is no `plugins` entry set.

## Usage

In your markdown documents you can now use:

```html
{{ read_csv('path_to_table.csv') }}
```

Where the path is relative to the location of your project's `mkdocs.yml` file.

Under the hood this is basically:

```python
import pandas as pd
df = pd.read_csv('path_to_table.csv')
df.to_markdown(index=False, tablefmt='pipe')
```

Which means you can pass all parameters of [pandas.read_csv()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html).

You can see an example usage in this repo (see `mkdocs.yml` and `docs/`) and the result at [timvink.github.io/mkdocs-table-reader-plugin/](https://timvink.github.io/mkdocs-table-reader-plugin/).

### Available readers

The following table reader functions are available:

- `{{ read_csv() }}` passed to [pandas.read_csv()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html).
- `{{ read_table() }}` passed to [pandas.read_table()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_table.html).
- `{{ read_fwf() }}` passed to [pandas.read_fwf()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_fwf.html).
- `{{ read_excel() }}` passed to [pandas.read_excel()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_excel.html).
- `{{ read_yaml() }}` is parsed with [yaml.safe_load()](https://pyyaml.org/wiki/PyYAMLDocumentation#loading-yaml) and passed to [pandas.json_normalize()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.json_normalize.html).

<details>
  <summary>Reading xlsx files</summary>
  
  You might get a `XLRDError('Excel xlsx file; not supported',)` error when trying to read modern excel files. That's because `xlrd` does not support `.xlsx` files ([stackoverflow post](https://stackoverflow.com/questions/65254535/xlrd-biffh-xlrderror-excel-xlsx-file-not-supported)). Instead, install [openpyxl](https://openpyxl.readthedocs.io/en/stable/) and use:

  `{{ read_excel('tables/excel_table.xlsx', engine='openpyxl') }}`
</details>

<details>
  <summary>Reading yaml variables</summary>

  [mkdocs-markdownextradata-plugin](https://github.com/rosscdh/mkdocs-markdownextradata-plugin) is a great plugin to use when working 
  with yaml files. It will read in all yaml files in a specified directory and make all keys available as jinja2 variables.
</details>

## Options

You can customize the plugin by setting options in `mkdocs.yml`. For example:

```yml
plugins:
  - table-reader:
      data_path: "docs"
```

#### `data_path`

Default is `.`, which means you can specify the path to your table files relative to the location of your project's `mkdocs.yml` file. If you use a folder for all your table files you can shorten the path specification by setting `data_path`.

For example, if you set `data_path` to `docs/` in the project below, you will be able to use `{{ read_csv("basic_table.csv") }}` instead of `{{ read_csv("docs/basic_table.csv") }}` inside `index.md`.

```nohighlight
.
├── docs
│   ├── basic_table.csv
│   └── index.md
└── mkdocs.yml
```

## Contributing

Contributions are very welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) before putting in any work.

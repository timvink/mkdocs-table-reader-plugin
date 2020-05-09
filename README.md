[![Actions Status](https://github.com/timvink/mkdocs-table-reader-plugin/workflows/pytest/badge.svg)](https://github.com/timvink/mkdocs-table-reader-plugin/actions)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mkdocs-table-reader-plugin)
![PyPI](https://img.shields.io/pypi/v/mkdocs-table-reader-plugin)
![PyPI - Downloads](https://img.shields.io/pypi/dm/mkdocs-table-reader-plugin)
[![codecov](https://codecov.io/gh/timvink/mkdocs-table-reader-plugin/branch/master/graph/badge.svg)](https://codecov.io/gh/timvink/mkdocs-table-reader-plugin)
![GitHub contributors](https://img.shields.io/github/contributors/timvink/mkdocs-table-reader-plugin)
![PyPI - License](https://img.shields.io/pypi/l/mkdocs-table-reader-plugin)

# mkdocs-table-reader-plugin

[MkDocs](https://www.mkdocs.org/) plugin that adds a `{{ read_csv('table.csv') }}` markdown tag to directly insert CSV files in a page.

This helps to enable building reproducible reports. For more complex use cases, consider [pheasant](https://pheasant.daizutabi.net/) or [nbconvert](https://tanbro.github.io/mkdocs-nbconvert/).

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
df.to_markdown(showindex=False)
```

Which means you can pass all parameters of [pandas.read_csv()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html).

### Available readers

The table reader functions implemented from `pandas`:

- `{{ read_csv() }}` passed to [pandas.read_csv()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html).
- `{{ read_table() }}` passed to [pandas.read_table()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_table.html)`.
- `{{ read_fwf() }}` passed to [pandas.read_fwf()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_fwf.html).
- `{{ read_excel() }}` passed to [pandas.read_excel()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_excel.html).

## Contributing

Contributions are very welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) before putting in any work.

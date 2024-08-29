[![Actions Status](https://github.com/timvink/mkdocs-table-reader-plugin/workflows/pytest/badge.svg)](https://github.com/timvink/mkdocs-table-reader-plugin/actions)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mkdocs-table-reader-plugin)
![PyPI](https://img.shields.io/pypi/v/mkdocs-table-reader-plugin)
![PyPI - Downloads](https://img.shields.io/pypi/dm/mkdocs-table-reader-plugin)
[![codecov](https://codecov.io/gh/timvink/mkdocs-table-reader-plugin/branch/master/graph/badge.svg)](https://codecov.io/gh/timvink/mkdocs-table-reader-plugin)
![GitHub contributors](https://img.shields.io/github/contributors/timvink/mkdocs-table-reader-plugin)
![PyPI - License](https://img.shields.io/pypi/l/mkdocs-table-reader-plugin)

# mkdocs-table-reader-plugin

[MkDocs](https://www.mkdocs.org/) plugin that enables a markdown tag like `{{ read_csv('table.csv') }}` to directly insert various table formats into a page. 

> For a workflow with other plugins see the blogpost [building reproducible reports with MkDocs](https://timvink.nl/reproducible-reports-with-mkdocs/)

## Installation

Install the plugin using `pip`:

```bash
pip install mkdocs-table-reader-plugin
```

Next, add the following lines to your `mkdocs.yml`:

```yml
plugins:
  - search
  - table-reader
```

> If you have no `plugins` entry in your config file yet, you'll likely also want to add the `search` plugin. MkDocs enables it by default if there is no `plugins` entry set.

## Usage

In your markdown files you can now use:

```html
{{ read_csv('path_to_table.csv') }}
```

Where the path is relative to the location of your project's `mkdocs.yml` file, _or_ your project's `docs/` directory, _or_ the location of your markdown source file (all 3 possible locations will be searched, in that order).

- There are [readers](https://timvink.github.io/mkdocs-table-reader-plugin/readers/) available for many common table formats, like `.csv`, `.fwf`, `.json`, `.xls`, `.xlsx`, `.yaml`, `.feather` and `.tsv`. There is also the `read_raw()` reader that will allow you to insert tables (or other content) already in markdown format.
- `table-reader` is compatible with [`mkdocs-macros-plugin`](https://mkdocs-macros-plugin.readthedocs.io/en/latest/). This enables further automation like filtering tables or inserting directories of tables. See the documentation on [compatibility with macros plugin](howto/use_jinja2.md) for more examples.

## Documentation and how-to guides

See [timvink.github.io/mkdocs-table-reader-plugin/](https://timvink.github.io/mkdocs-table-reader-plugin/)

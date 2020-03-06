# mkdocs-git-authors-plugin

[MkDocs](https://www.mkdocs.org/) plugin that adds a `read_csv(path)` markdown tag to directly insert CSV files in a page.

This will aid building with reproducible sites. For more complex use cases, consider [pheasant](https://pheasant.daizutabi.net/) or [nbconvert](https://tanbro.github.io/mkdocs-nbconvert/).

## Setup

Install the plugin using pip:

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

In your markdown documents you can now use:

```html
{{ read_csv('path_to_table.csv') }}
```

Where the path is relative to your project's root. 

Under the hood this is basically:

```python
import pandas as pd
df = pd.read_csv(path)
df.to_markdown(showindex=False)
```

Which means you can pass all parameters of [pandas.read_csv()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html).

### Available readers

Table reader functions implemented from `pandas`: 

- `{{ read_csv() }}` passed to [pandas.read_csv()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html).
- `{{ read_table() }}` passed to [pandas.read_table()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_table.html)`.
- `{{ read_fwf() }}` passed to [pandas.read_fwf()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_fwf.html).
- `{{ read_excel() }}` passed to [pandas.read_excel()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_excel.html).

## Contributing

Very much open to contributions! Please read [CONTRIBUTING.md](CONTRIBUTING.md) before putting in any work.
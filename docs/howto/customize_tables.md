# Customize markdown tables

You can customize the resulting markdown tables! 

## Theory

Under the hood `mkdocs-table-reader-plugin` is basically doing:

```python
import pandas as pd
df = pd.read_csv('path_to_table.csv')
df.to_markdown(index=False, tablefmt='pipe')
```

{% raw %}
Any keyword arguments you give to `{{ read_csv('path_to_your_table.csv') }}` will be matched and passed the corresponding [pandas.read_csv()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html) and/or 
[.to_markdown()](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_markdown.html) functions. 
{% endraw %}

Pandas's `.to_markdown()` uses the [tabulate](https://pypi.org/project/tabulate/) package and any keyword arguments that are passed to it. Tabulate in turn offers many customization options, see [library usage](https://github.com/astanin/python-tabulate#library-usage). 

## Aligning columns

Text columns will be aligned to the left [by default](https://github.com/astanin/python-tabulate#column-alignment), whilst columns which contain only numbers will be aligned to the right. You can override this behaviour using [tabulate](https://pypi.org/project/tabulate/)'s [custom column alignment](https://github.com/astanin/python-tabulate#custom-column-alignment). Example:

=== ":arrow_left: left"

    {% raw %}
    ```
    {{ read_csv('tables/basic_table.csv', colalign=("left",)) }}
    ```
    {% endraw %}

    {{ read_csv('tables/basic_table.csv', colalign=("left",)) | add_indentation(spaces=4) }}

=== ":left_right_arrow: center"

    {% raw %}
    ```
    {{ read_csv('tables/basic_table.csv', colalign=("center",)) }}
    ```
    {% endraw %}

    {{ read_csv('tables/basic_table.csv', colalign=("center",)) | add_indentation(spaces=4) }}

=== ":arrow_right: right"

    {% raw %}
    ```
    {{ read_csv('tables/basic_table.csv', colalign=("right",)) }}
    ```
    {% endraw %}

    {{ read_csv('tables/basic_table.csv', colalign=("right",)) | add_indentation(spaces=4) }}

## Sortable tables

If you use [mkdocs-material](https://squidfunk.github.io/mkdocs-material), you can configure [sortable tables](https://squidfunk.github.io/mkdocs-material/reference/data-tables/?h=tables#sortable-tables).

## Number formatting

You can use [tabulate](https://pypi.org/project/tabulate/)'s [number formatting](https://github.com/astanin/python-tabulate#number-formatting). Example:

=== "zero points"

    {% raw %}
    ```
    {{ read_fwf('tables/fixedwidth_table.txt', floatfmt=".0f") }}
    ```
    {% endraw %}

    {{ read_fwf('tables/fixedwidth_table.txt', floatfmt=".0f") | add_indentation(spaces=4) }}

=== "one points"

    {% raw %}
    ```
    {{ read_fwf('tables/fixedwidth_table.txt', floatfmt=".1f") }}
    ```
    {% endraw %}

    {{ read_fwf('tables/fixedwidth_table.txt', floatfmt=".1f") | add_indentation(spaces=4) }}

=== "two points"

    {% raw %}
    ```
    {{ read_fwf('tables/fixedwidth_table.txt', floatfmt=".2f") }}
    ```
    {% endraw %}

    {{ read_fwf('tables/fixedwidth_table.txt', floatfmt=".2f") | add_indentation(spaces=4) }}


## Further customization

If you use enable [`mkdocs-macros-plugin`](https://mkdocs-macros-plugin.readthedocs.io/en/latest/) (see [ Compatibility with mkdocs-macros-plugin to enable further automation](use_jinja2.md)), you can do much more.

For example, you could insert images from base64 encodings in a table like so:

{% raw %}
```jinja
{% for base64_image in pd_read_csv('tables/html_table.csv', sep=";")['a'] %}

<img src="data:image/png;base64,{{ base64_image }}" alt="Small Red Dot">

{% endfor %}
```
{% endraw %}

Should render 3 smileys:

{% for base64_image in pd_read_csv('tables/html_table.csv', sep=";")['a'] %}

<img src="data:image/png;base64,{{ base64_image }}" alt="Small Red Dot">

{% endfor %}


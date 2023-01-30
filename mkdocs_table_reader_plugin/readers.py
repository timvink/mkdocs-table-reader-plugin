import pandas as pd
import yaml

from mkdocs_table_reader_plugin.utils import kwargs_in_func, kwargs_not_in_func 
from mkdocs_table_reader_plugin.markdown import convert_to_md_table

def read_csv(*args, **kwargs):
    
    read_kwargs = kwargs_in_func(kwargs, pd.read_csv)
    df = pd.read_csv(*args, **read_kwargs)

    markdown_kwargs = kwargs_not_in_func(kwargs, pd.read_csv)
    return convert_to_md_table(df, markdown_kwargs)


def read_table(*args, **kwargs):

    read_kwargs = kwargs_in_func(kwargs, pd.read_table)
    df = pd.read_table(*args, **read_kwargs)

    markdown_kwargs = kwargs_not_in_func(kwargs, pd.read_table)
    return convert_to_md_table(df, markdown_kwargs)


def read_fwf(*args, **kwargs):
    read_kwargs = kwargs_in_func(kwargs, pd.read_fwf)
    df = pd.read_fwf(*args, **read_kwargs)

    markdown_kwargs = kwargs_not_in_func(kwargs, pd.read_fwf)
    return convert_to_md_table(df, markdown_kwargs)

def read_json(*args, **kwargs):
    read_kwargs = kwargs_in_func(kwargs, pd.read_json)
    df = pd.read_json(*args, **read_kwargs)

    markdown_kwargs = kwargs_not_in_func(kwargs, pd.read_json)
    return convert_to_md_table(df, markdown_kwargs)


def read_excel(*args, **kwargs):
    read_kwargs = kwargs_in_func(kwargs, pd.read_excel)
    df = pd.read_excel(*args, **read_kwargs)

    markdown_kwargs = kwargs_not_in_func(kwargs, pd.read_excel)
    return convert_to_md_table(df, markdown_kwargs)


def read_yaml(*args, **kwargs):

    json_kwargs = kwargs_in_func(kwargs, pd.json_normalize)
    with open(args[0], "r") as f:
        df = pd.json_normalize(yaml.safe_load(f), **json_kwargs)

    markdown_kwargs = kwargs_not_in_func(kwargs, pd.json_normalize)
    return convert_to_md_table(df, markdown_kwargs)

def read_raw(*args, **kwargs):
    """Read a file as-is.

    Returns:
        str: file contents
    """
    with open(args[0], "r") as f:
        return f.read()


READERS = {
    "read_csv": read_csv,
    "read_table": read_table,
    "read_fwf": read_fwf,
    "read_excel": read_excel,
    "read_yaml": read_yaml,
    "read_json": read_json,
    "read_raw": read_raw,
}


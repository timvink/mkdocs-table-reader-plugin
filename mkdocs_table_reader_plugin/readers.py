import os
import re
import pandas as pd
import yaml
import textwrap
from inspect import signature 

from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options
from mkdocs.exceptions import ConfigurationError

from mkdocs_table_reader_plugin.safe_eval import parse_argkwarg
from mkdocs_table_reader_plugin.utils import get_keywords, kwargs_in_func, kwargs_not_in_func 

def read_csv(*args, **kwargs):
    
    read_kwargs = kwargs_in_func(kwargs, pd.read_csv)
    df = pd.read_csv(*args, **read_kwargs)

    markdown_kwargs = kwargs_not_in_func(kwargs, pd.read_csv)
    if "index" not in markdown_kwargs:
        markdown_kwargs["index"] = False
    if "tablefmt" not in markdown_kwargs:
        markdown_kwargs["tablefmt"] = "pipe"
    
    return df.to_markdown(**markdown_kwargs)


def read_table(*args, **kwargs):

    read_kwargs = kwargs_in_func(kwargs, pd.read_table)
    df = pd.read_table(*args, **read_kwargs)

    markdown_kwargs = kwargs_not_in_func(kwargs, pd.read_table)
    if "index" not in markdown_kwargs:
        markdown_kwargs["index"] = False
    if "tablefmt" not in markdown_kwargs:
        markdown_kwargs["tablefmt"] = "pipe"
    
    return df.to_markdown(**markdown_kwargs)


def read_fwf(*args, **kwargs):
    read_kwargs = kwargs_in_func(kwargs, pd.read_fwf)
    df = pd.read_fwf(*args, **read_kwargs)

    markdown_kwargs = kwargs_not_in_func(kwargs, pd.read_fwf)
    if "index" not in markdown_kwargs:
        markdown_kwargs["index"] = False
    if "tablefmt" not in markdown_kwargs:
        markdown_kwargs["tablefmt"] = "pipe"
    
    return df.to_markdown(**markdown_kwargs)

def read_json(*args, **kwargs):
    read_kwargs = kwargs_in_func(kwargs, pd.read_json)
    df = pd.read_json(*args, **read_kwargs)

    markdown_kwargs = kwargs_not_in_func(kwargs, pd.read_json)
    if "tablefmt" not in markdown_kwargs:
        markdown_kwargs["tablefmt"] = "pipe"
    
    return df.to_markdown(**markdown_kwargs)


def read_excel(*args, **kwargs):
    read_kwargs = kwargs_in_func(kwargs, pd.read_excel)
    df = pd.read_excel(*args, **read_kwargs)

    markdown_kwargs = kwargs_not_in_func(kwargs, pd.read_excel)
    if "index" not in markdown_kwargs:
        markdown_kwargs["index"] = False
    if "tablefmt" not in markdown_kwargs:
        markdown_kwargs["tablefmt"] = "pipe"
        
    return df.to_markdown(**markdown_kwargs)


def read_yaml(*args, **kwargs):

    json_kwargs = kwargs_in_func(kwargs, pd.json_normalize)
    with open(args[0], "r") as f:
        df = pd.json_normalize(yaml.safe_load(f), **json_kwargs)

    markdown_kwargs = kwargs_not_in_func(kwargs, pd.json_normalize)
    if "index" not in markdown_kwargs:
        markdown_kwargs["index"] = False
    if "tablefmt" not in markdown_kwargs:
        markdown_kwargs["tablefmt"] = "pipe"
    
    return df.to_markdown(**markdown_kwargs)


READERS = {
    "read_csv": read_csv,
    "read_table": read_table,
    "read_fwf": read_fwf,
    "read_excel": read_excel,
    "read_yaml": read_yaml,
    "read_json": read_json,
}


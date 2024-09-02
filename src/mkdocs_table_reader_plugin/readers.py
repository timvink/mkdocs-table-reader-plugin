import functools
import logging
import os
from pathlib import Path

import pandas as pd
import yaml

from mkdocs_table_reader_plugin.markdown import convert_to_md_table
from mkdocs_table_reader_plugin.utils import kwargs_in_func, kwargs_not_in_func

logger = logging.getLogger("mkdocs.plugins")


class ParseArgs:
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func
        self.mkdocs_config = None
        self.plugin_config = None

    def set_config_context(self, mkdocs_config, plugin_config):
        self.mkdocs_config = mkdocs_config
        self.plugin_config = plugin_config
        return self

    def __call__(self, *args, **kwargs):
        assert self.mkdocs_config is not None, "mkdocs_config is not set"
        assert self.plugin_config is not None, "plugin_config is not set"

        # Extract the filepath,
        # which is the first positional argument
        # or a named argument when there are no positional arguments
        args = list(args)
        if len(args) > 0:
            input_file_name = args.pop(0)
        else:
            input_file_name = kwargs.pop("filepath_or_buffer")

        possible_file_paths = [
            Path(
                os.path.dirname(os.path.abspath(self.mkdocs_config["config_file_path"]))
            )
            / Path(self.plugin_config.get("data_path"))
            / input_file_name,
            Path(os.path.abspath(self.mkdocs_config["docs_dir"]))
            / Path(self.plugin_config.get("data_path"))
            / input_file_name,
            Path(self.plugin_config._current_page).parent / input_file_name,
        ]
        valid_file_paths = [path for path in possible_file_paths if path.exists()]
        if len(valid_file_paths) == 0:
            msg = f"[table-reader-plugin]: Cannot find table file '{input_file_name}'. The following directories were searched: {*possible_file_paths,}"
            if self.plugin_config.get("allow_missing_files"):
                logger.warning(msg)
                return f"{{{{ Cannot find '{input_file_name}' }}}}"
            else:
                raise FileNotFoundError(msg)

        return self.func(valid_file_paths[0], *args, **kwargs)


@ParseArgs
def pd_read_csv(*args, **kwargs) -> str:
    read_kwargs = kwargs_in_func(kwargs, pd.read_csv)
    return pd.read_csv(*args, **read_kwargs)

@ParseArgs
def read_csv(*args, **kwargs) -> str:
    read_kwargs = kwargs_in_func(kwargs, pd.read_csv)
    df = pd.read_csv(*args, **read_kwargs)

    markdown_kwargs = kwargs_not_in_func(kwargs, pd.read_csv)
    return convert_to_md_table(df, **markdown_kwargs)


@ParseArgs
def pd_read_table(*args, **kwargs) -> str:
    read_kwargs = kwargs_in_func(kwargs, pd.read_table)
    return pd.read_table(*args, **read_kwargs)

@ParseArgs
def read_table(*args, **kwargs) -> str:
    read_kwargs = kwargs_in_func(kwargs, pd.read_table)
    df = pd.read_table(*args, **read_kwargs)

    markdown_kwargs = kwargs_not_in_func(kwargs, pd.read_table)
    return convert_to_md_table(df, **markdown_kwargs)


@ParseArgs
def pd_read_fwf(*args, **kwargs) -> str:
    read_kwargs = kwargs_in_func(kwargs, pd.read_fwf)
    return pd.read_fwf(*args, **read_kwargs)


@ParseArgs
def read_fwf(*args, **kwargs) -> str:
    read_kwargs = kwargs_in_func(kwargs, pd.read_fwf)
    df = pd.read_fwf(*args, **read_kwargs)

    markdown_kwargs = kwargs_not_in_func(kwargs, pd.read_fwf)
    return convert_to_md_table(df, **markdown_kwargs)

@ParseArgs
def pd_read_json(*args, **kwargs) -> str:
    read_kwargs = kwargs_in_func(kwargs, pd.read_json)
    return pd.read_json(*args, **read_kwargs)


@ParseArgs
def read_json(*args, **kwargs) -> str:
    read_kwargs = kwargs_in_func(kwargs, pd.read_json)
    df = pd.read_json(*args, **read_kwargs)

    markdown_kwargs = kwargs_not_in_func(kwargs, pd.read_json)
    return convert_to_md_table(df, **markdown_kwargs)

@ParseArgs
def pd_read_excel(*args, **kwargs) -> str:
    read_kwargs = kwargs_in_func(kwargs, pd.read_excel)
    return pd.read_excel(*args, **read_kwargs)


@ParseArgs
def read_excel(*args, **kwargs) -> str:
    read_kwargs = kwargs_in_func(kwargs, pd.read_excel)
    df = pd.read_excel(*args, **read_kwargs)

    markdown_kwargs = kwargs_not_in_func(kwargs, pd.read_excel)
    return convert_to_md_table(df, **markdown_kwargs)


@ParseArgs
def pd_read_yaml(*args, **kwargs) -> str:
    json_kwargs = kwargs_in_func(kwargs, pd.json_normalize)
    with open(args[0]) as f:
        df = pd.json_normalize(yaml.safe_load(f), **json_kwargs)
    return df

@ParseArgs
def read_yaml(*args, **kwargs) -> str:
    json_kwargs = kwargs_in_func(kwargs, pd.json_normalize)
    with open(args[0]) as f:
        df = pd.json_normalize(yaml.safe_load(f), **json_kwargs)

    markdown_kwargs = kwargs_not_in_func(kwargs, pd.json_normalize)
    return convert_to_md_table(df, **markdown_kwargs)


@ParseArgs
def pd_read_feather(*args, **kwargs) -> str:
    read_kwargs = kwargs_in_func(kwargs, pd.read_feather)
    return pd.read_feather(*args, **read_kwargs)


@ParseArgs
def read_feather(*args, **kwargs) -> str:
    read_kwargs = kwargs_in_func(kwargs, pd.read_feather)
    df = pd.read_feather(*args, **read_kwargs)

    markdown_kwargs = kwargs_not_in_func(kwargs, pd.read_feather)
    return convert_to_md_table(df, **markdown_kwargs)


@ParseArgs
def read_raw(*args, **kwargs) -> str:
    """Read a file as-is.

    Returns:
        str: file contents
    """
    with open(args[0]) as f:
        return f.read()


READERS = {
    "read_csv": read_csv,
    "read_table": read_table,
    "read_fwf": read_fwf,
    "read_excel": read_excel,
    "read_yaml": read_yaml,
    "read_json": read_json,
    "read_feather": read_feather,
    "read_raw": read_raw,
}

MACRO_ONLY = {
    "pd_read_csv": pd_read_csv,
    "pd_read_table": pd_read_table,
    "pd_read_fwf": pd_read_fwf,
    "pd_read_excel": pd_read_excel,
    "pd_read_yaml": pd_read_yaml,
    "pd_read_json": pd_read_json,
    "pd_read_feather": pd_read_feather,
}
MACROS = {**READERS, **MACRO_ONLY}
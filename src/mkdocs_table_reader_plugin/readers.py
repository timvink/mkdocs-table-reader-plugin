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


def read_yaml_file(filepath, encoding: str = "utf-8", **kwargs) -> pd.DataFrame:
    """
    Read a YAML file into a pd.DataFrame.

    The contents are parsed with yaml.safe_load() and passed to pd.json_normalize().
    """
    with open(filepath, encoding=encoding) as f:
        return pd.json_normalize(yaml.safe_load(f), **kwargs)


def read_html_file(*args, **kwargs) -> pd.DataFrame:
    """
    Read the first table of an HTML file into a pd.DataFrame.

    pd.read_html() returns all tables it finds, use the 'match' argument to select one.
    """
    return pd.read_html(*args, **kwargs)[0]


def read_hdf_file(*args, **kwargs) -> pd.DataFrame:
    """
    Read a HDF5 file into a pd.DataFrame.

    pd.read_hdf() returns a pd.Series when a Series was stored.
    """
    data = pd.read_hdf(*args, **kwargs)
    if isinstance(data, pd.Series):
        data = data.to_frame()
    return data


def markdown_reader(load_function, *extra_kwarg_sources) -> ParseArgs:
    """
    Create a reader that inserts a file as a markdown table.

    Args:
        load_function: function that reads a file path into a pd.DataFrame
        extra_kwarg_sources: functions with additional keyword arguments accepted
            by load_function, on top of its own. Any other keyword arguments are
            passed on to pd.DataFrame.to_markdown()

    Returns:
        ParseArgs: reader that returns a markdown table
    """
    kwarg_sources = (load_function, *extra_kwarg_sources)

    @functools.wraps(load_function)
    def reader(*args, **kwargs) -> str:
        df = load_function(*args, **kwargs_in_func(kwargs, *kwarg_sources))
        markdown_kwargs = kwargs_not_in_func(kwargs, *kwarg_sources)
        return convert_to_md_table(df, **markdown_kwargs)

    return ParseArgs(reader)


def dataframe_reader(load_function, *extra_kwarg_sources) -> ParseArgs:
    """
    Create a macro that returns a file as a pd.DataFrame.

    Args:
        load_function: function that reads a file path into a pd.DataFrame
        extra_kwarg_sources: functions with additional keyword arguments accepted
            by load_function, on top of its own

    Returns:
        ParseArgs: reader that returns a pd.DataFrame
    """
    kwarg_sources = (load_function, *extra_kwarg_sources)

    @functools.wraps(load_function)
    def reader(*args, **kwargs) -> pd.DataFrame:
        return load_function(*args, **kwargs_in_func(kwargs, *kwarg_sources))

    return ParseArgs(reader)


@ParseArgs
def read_raw(*args, **kwargs) -> str:
    """Read a file as-is.

    Returns:
        str: file contents
    """
    encoding = kwargs.pop("encoding", "utf-8")
    with open(args[0], encoding=encoding) as f:
        return f.read()


# The function used to load each file format into a pd.DataFrame,
# optionally followed by functions with additional keyword arguments it accepts.
LOADERS = {
    "read_csv": (pd.read_csv,),
    "read_table": (pd.read_table,),
    "read_fwf": (pd.read_fwf,),
    "read_excel": (pd.read_excel,),
    "read_yaml": (read_yaml_file, pd.json_normalize),
    "read_json": (pd.read_json,),
    "read_feather": (pd.read_feather,),
    "read_parquet": (pd.read_parquet,),
    "read_orc": (pd.read_orc,),
    "read_html": (read_html_file, pd.read_html),
    "read_xml": (pd.read_xml,),
    "read_hdf": (read_hdf_file, pd.read_hdf),
    "read_sas": (pd.read_sas,),
    "read_spss": (pd.read_spss,),
    "read_stata": (pd.read_stata,),
}

READERS = {name: markdown_reader(*loader) for name, loader in LOADERS.items()}
READERS["read_raw"] = read_raw

MACRO_ONLY = {f"pd_{name}": dataframe_reader(*loader) for name, loader in LOADERS.items()}

MACROS = {**READERS, **MACRO_ONLY}

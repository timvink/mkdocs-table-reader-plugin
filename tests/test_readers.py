import pandas as pd

from mkdocs_table_reader_plugin.readers import LOADERS, MACROS, READERS, read_yaml_file
from mkdocs_table_reader_plugin.utils import kwargs_in_func, kwargs_not_in_func


def test_readers():
    # every reader has a macro that returns a pd.DataFrame instead of a markdown table
    assert set(READERS) == set(LOADERS) | {"read_raw"}
    assert set(MACROS) == set(READERS) | {f"pd_{reader}" for reader in LOADERS}


def test_reader_kwargs():
    # read_yaml() accepts the arguments of both read_yaml_file() and pd.json_normalize()
    kwargs = {"encoding": "cp1251", "max_level": 1, "tablefmt": "github"}
    sources = (read_yaml_file, pd.json_normalize)

    assert kwargs_in_func(kwargs, *sources) == {"encoding": "cp1251", "max_level": 1}
    # anything else is passed on to .to_markdown()
    assert kwargs_not_in_func(kwargs, *sources) == {"tablefmt": "github"}

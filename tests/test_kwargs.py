
import pandas as pd 
from mkdocs_table_reader_plugin.utils import get_keywords, kwargs_in_func, kwargs_not_in_func
from mkdocs_table_reader_plugin.safe_eval import parse_argkwarg


def test_kwargs():

    assert 'sep' in get_keywords(pd.read_csv)    

    keywords = {'hi' : 'there', 'sep' : ";"}

    assert kwargs_in_func(keywords, pd.read_csv) == {'sep' : ';'}
    assert kwargs_not_in_func(keywords, pd.read_csv) == {'hi' : 'there'}


def test_parse_argkwarg():

    assert parse_argkwarg("sep=';'") == ([], {'sep': ';'})
    assert parse_argkwarg('"file.csv", usecols=["A", "B"]') == (['file.csv'], {'usecols': ['A', 'B']})
    assert parse_argkwarg('"file.csv", usecols=[\'A\',\'B\']') == (['file.csv'], {'usecols': ['A', 'B']})
    assert parse_argkwarg("'assets/tables/table_with_carriage_return.csv', sep = ','") == (['assets/tables/table_with_carriage_return.csv'], {'sep': ','})
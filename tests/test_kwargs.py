
import pandas as pd 
from mkdocs_table_reader_plugin.utils import get_keywords, kwargs_in_func, kwargs_not_in_func


def test_kwargs():

    assert 'sep' in get_keywords(pd.read_csv)    

    keywords = {'hi' : 'there', 'sep' : ";"}

    assert kwargs_in_func(keywords, pd.read_csv) == {'sep' : ';'}
    assert kwargs_not_in_func(keywords, pd.read_csv) == {'hi' : 'there'}


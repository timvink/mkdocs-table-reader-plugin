import pandas as pd
from mkdocs_table_reader_plugin.markdown import convert_to_md_table, replace_unescaped_pipes


def test_unescaped_pipes():
    assert replace_unescaped_pipes("hi|there\\|you|there") == "hi\\|there\\|you\\|there"


def test_convert_to_md_table():

    df_bad = pd.read_csv("tests/fixtures/csv_with_pipes/docs/example_unescaped.csv")
    df_good = pd.read_csv("tests/fixtures/csv_with_pipes/docs/example_escaped.csv")
    assert df_bad.shape[0] > 0
    assert df_good.shape[0] > 0

    # Because we escape pipes, the 'bad' df
    md_bad = convert_to_md_table(df_bad, markdown_kwargs={})
    md_good = convert_to_md_table(df_good, markdown_kwargs={})
    assert md_bad == md_good
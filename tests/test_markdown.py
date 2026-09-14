import pandas as pd

from mkdocs_table_reader_plugin.markdown import (
    convert_to_md_table,
    replace_newlines,
    replace_unescaped_pipes,
)


def test_unescaped_pipes():
    assert replace_unescaped_pipes("hi|there\\|you|there") == "hi\\|there\\|you\\|there"


def test_replace_newlines():
    assert replace_newlines("one\ntwo") == "one<br>two"
    assert replace_newlines("one\r\ntwo") == "one<br>two"
    assert replace_newlines("one\rtwo") == "one<br>two"
    assert replace_newlines("one\n\ntwo") == "one<br><br>two"
    assert replace_newlines("no newlines here") == "no newlines here"


def test_convert_to_md_table():

    df_bad = pd.read_csv("tests/fixtures/csv_with_pipes/docs/example_unescaped.csv")
    df_good = pd.read_csv("tests/fixtures/csv_with_pipes/docs/example_escaped.csv")
    assert df_bad.shape[0] > 0
    assert df_good.shape[0] > 0

    # Because we escape pipes, the 'bad' df
    md_bad = convert_to_md_table(df_bad, **{})
    md_good = convert_to_md_table(df_good, **{})
    assert md_bad == md_good


def test_convert_to_md_table_multiline():
    """
    A multiline cell should not break up a markdown table.

    See https://github.com/timvink/mkdocs-table-reader-plugin/issues/83
    """
    df = pd.read_csv("tests/fixtures/csv_multiline/docs/example_multiline.csv")
    assert df.shape == (2, 3)

    md = convert_to_md_table(df, **{})
    assert "Sometimes the cell text is quoted.<br><br>But not always" in md
    # A header, a separator and one line per record
    assert len(md.split("\n")) == 4


def test_convert_to_md_table_multiline_other_tablefmt():
    """
    Table formats that display multiline cells themselves are left alone.
    """
    df = pd.read_csv("tests/fixtures/csv_multiline/docs/example_multiline.csv")

    md = convert_to_md_table(df, tablefmt="grid")
    assert "<br>" not in md
    assert "Sometimes the cell text is quoted." in md
    assert "But not always" in md

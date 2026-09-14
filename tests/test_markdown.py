import pandas as pd
import pytest

from mkdocs_table_reader_plugin.markdown import (
    add_indentation,
    convert_to_md_table,
    fix_indentation,
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


def test_add_indentation():
    """
    The filter used with mkdocs-macros-plugin, which strips indentation itself.
    """
    table = "| a |\n|---|\n| 1 |"

    # Surrounded by newlines, so the table starts on a line of its own
    assert add_indentation(table) == f"\n{table}\n"
    assert add_indentation(table, spaces=4) == "\n    | a |\n    |---|\n    | 1 |\n"
    assert add_indentation(table, tabs=1) == "\n\t| a |\n\t|---|\n\t| 1 |\n"

    # Empty lines are left empty, instead of becoming trailing whitespace
    assert add_indentation("a\n\nb", spaces=2) == "\n  a\n\n  b\n"


def test_add_indentation_spaces_and_tabs():
    with pytest.raises(ValueError):
        add_indentation("| a |", spaces=4, tabs=1)


def test_fix_indentation():
    """
    The indentation of a tag is applied to the table that replaces it.
    """
    table = "| a |\n|---|\n| 1 |"

    assert fix_indentation(table, leading_spaces="") == table
    assert fix_indentation(table, leading_spaces="    ") == "    | a |\n    |---|\n    | 1 |"
    assert fix_indentation(table, leading_spaces="\t") == table

    # Rounded down to a multiple of 4 spaces, which is one markdown indentation level
    assert fix_indentation(table, leading_spaces="  ") == table
    assert fix_indentation(table, leading_spaces="      ") == fix_indentation(table, leading_spaces="    ")


def test_convert_to_md_table_does_not_alter_input():
    """
    Escaping happens on a copy, because macros users can render a DataFrame twice.
    """
    df = pd.DataFrame({"a|b": ["x|y"]})

    first = convert_to_md_table(df)

    assert list(df.columns) == ["a|b"]
    assert df.iloc[0, 0] == "x|y"
    # So a second render escapes the same pipes once, not twice
    assert convert_to_md_table(df) == first

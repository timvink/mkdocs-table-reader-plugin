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


@pytest.mark.parametrize("tablefmt", ["pipe", "github"])
@pytest.mark.parametrize("newline", ["\n", "\r\n", "\r"])
def test_convert_to_md_table_index(tablefmt, newline):
    df = pd.DataFrame(
        {"value": [1, 2]},
        index=pd.Index(["a|b", f"two{newline}lines"], name=f"row|{newline}name"),
    )
    original = df.copy(deep=True)

    md = convert_to_md_table(df, index=True, tablefmt=tablefmt)

    assert "a\\|b" in md
    assert "two<br>lines" in md
    assert "row\\|<br>name" in md
    assert len(md.splitlines()) == 4
    pd.testing.assert_frame_equal(df, original)
    assert convert_to_md_table(df, index=True, tablefmt=tablefmt) == md


@pytest.mark.parametrize("tablefmt", ["pipe", "github"])
def test_convert_to_md_table_index_preescaped_pipes(tablefmt):
    df = pd.DataFrame({"value": [1]}, index=pd.Index([r"a\|b"], name=r"row\|name"))

    md = convert_to_md_table(df, index=True, tablefmt=tablefmt)

    assert r"a\|b" in md
    assert r"row\|name" in md
    assert r"a\\|b" not in md
    assert r"row\\|name" not in md


def test_convert_to_md_table_index_grid():
    df = pd.DataFrame({"value": [1]}, index=pd.Index(["a|b\ntwo"], name="row|name"))

    md = convert_to_md_table(df, index=True, tablefmt="grid")

    assert "<br>" not in md
    assert r"a\|b" in md
    assert "two" in md
    assert r"row\|name" in md


@pytest.mark.parametrize(
    "index",
    [
        pd.Index([1, 2], name="row"),
        pd.Index([1.25, 2.5], name="row"),
        pd.date_range("2026-01-01", periods=2, name="row"),
        pd.CategoricalIndex(["a", "b"], name="row"),
        pd.Index(["a", None], dtype=object, name="row"),
        pd.Index([(1, "a"), (2, "b")], name="row", tupleize_cols=False),
        pd.MultiIndex.from_tuples([(1, "a"), (2, "b")], names=["number", "letter"]),
    ],
)
def test_convert_to_md_table_index_types(index):
    df = pd.DataFrame({"value": [1, 2]}, index=index)
    original = df.copy(deep=True)

    assert convert_to_md_table(df, index=True, floatfmt=".1f") == df.to_markdown(index=True, floatfmt=".1f")
    pd.testing.assert_frame_equal(df, original)


def test_convert_to_md_table_hidden_index():
    df = pd.DataFrame({"value": [1]}, index=pd.Index(["a|b\ntwo"], name="row|name"))
    original = df.copy(deep=True)

    assert convert_to_md_table(df, index=False) == df.to_markdown(index=False)
    pd.testing.assert_frame_equal(df, original)


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

import re
import textwrap

import pandas as pd

# Table formats that render each row on a single line, and therefore cannot
# contain literal newlines. See https://github.com/timvink/mkdocs-table-reader-plugin/issues/83
SINGLE_LINE_TABLE_FORMATS = ("pipe", "github")


def replace_unescaped_pipes(text: str) -> str:
    """
    Replace unescaped pipes.

    For regex explanation, see https://regex101.com/r/s8H588/1

    Args:
        text (str): input string

    Returns:
        str: output string
    """
    return re.sub(r"(?<!\\)\|", "\\|", text)


def replace_newlines(text: str) -> str:
    """
    Replace newlines with <br>.

    A markdown table row must fit on a single line, so a cell that contains a
    newline (as multiline CSV cells do) would otherwise break up the table.

    Args:
        text (str): input string

    Returns:
        str: output string
    """
    return re.sub(r"\r\n|\r|\n", "<br>", text)


def convert_to_md_table(df: pd.DataFrame, **markdown_kwargs: dict) -> str:
    """
    Convert dataframe to markdown table using tabulate.
    """
    if "index" not in markdown_kwargs:
        markdown_kwargs["index"] = False
    if "tablefmt" not in markdown_kwargs:
        markdown_kwargs["tablefmt"] = "pipe"

    # Escape any pipe characters, | to \|
    # See https://github.com/astanin/python-tabulate/issues/241
    # And replace newlines with <br>, but only for table formats that need it:
    # formats like 'grid' display multiline cells just fine.
    escape_newlines = markdown_kwargs["tablefmt"] in SINGLE_LINE_TABLE_FORMATS

    def escape(value):
        if not isinstance(value, str):
            return value
        value = replace_unescaped_pipes(value)
        if escape_newlines:
            value = replace_newlines(value)
        return value

    # Escape a copy, so that a DataFrame passed in by a macros user is left alone
    df = df.map(escape)
    df.columns = [escape(c) for c in df.columns]

    return df.to_markdown(**markdown_kwargs)


def add_indentation(text: str, *, spaces: int = 0, tabs: int = 0) -> str:
    """
    Adds indentation to a text.

    Args:
        spaces (int): Indentation to add in spaces
        tabs (int): Indentation to add in tabs
        text (str): input text

    Returns:
        str: fixed text
    """
    if spaces and tabs:
        raise ValueError("You can only specify either spaces or tabs, not both.")
    if spaces:
        indentation = " " * spaces
    elif tabs:
        indentation = "\t" * tabs
    else:
        indentation = ""

    fixed_lines = []
    for line in text.split("\n"):
        fixed_lines.append(textwrap.indent(line, indentation))
    text = "\n" + "\n".join(fixed_lines) + "\n"
    
    return text


def fix_indentation(text: str, *, leading_spaces: str) -> str:
    """
    Adds indentation to a text.

    Args:
        leading_spaces (str): Indentation to add in actual spaces, e.g. "    " for 4 spaces
        text (str): input text

    Returns:
        str: fixed text
    """
    # make sure it's in multiples of 4 spaces
    leading_spaces = int(len(leading_spaces) / 4) * "    "

    fixed_lines = []
    for line in text.split("\n"):
        fixed_lines.append(textwrap.indent(line, leading_spaces))
    text = "\n".join(fixed_lines)
    return text

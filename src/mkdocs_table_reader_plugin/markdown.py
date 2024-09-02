import re
import textwrap

import pandas as pd


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


def convert_to_md_table(df: pd.DataFrame, **markdown_kwargs: dict) -> str:
    """
    Convert dataframe to markdown table using tabulate.
    """
    # Escape any pipe characters, | to \|
    # See https://github.com/astanin/python-tabulate/issues/241
    df.columns = [
        replace_unescaped_pipes(c) if isinstance(c, str) else c for c in df.columns
    ]

    # Avoid deprecated applymap warning on pandas>=2.0
    # See https://github.com/timvink/mkdocs-table-reader-plugin/issues/55
    if pd.__version__ >= "2.1.0":
        df = df.map(lambda s: replace_unescaped_pipes(s) if isinstance(s, str) else s)
    else:
        df = df.applymap(
            lambda s: replace_unescaped_pipes(s) if isinstance(s, str) else s
        )

    if "index" not in markdown_kwargs:
        markdown_kwargs["index"] = False
    if "tablefmt" not in markdown_kwargs:
        markdown_kwargs["tablefmt"] = "pipe"

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

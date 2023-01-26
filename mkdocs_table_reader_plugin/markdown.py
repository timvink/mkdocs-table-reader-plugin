import re
from typing import Dict
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


def convert_to_md_table(df: pd.DataFrame, markdown_kwargs: Dict) -> str:
    """
    Convert dataframe to markdown table using tabulate.
    """
    # Escape any pipe characters, | to \|
    # See https://github.com/astanin/python-tabulate/issues/241
    df.columns = [replace_unescaped_pipes(c) for c in df.columns]
    df = df.applymap(lambda s: replace_unescaped_pipes(s) if isinstance(s, str) else s)

    if "index" not in markdown_kwargs:
        markdown_kwargs["index"] = False
    if "tablefmt" not in markdown_kwargs:
        markdown_kwargs["tablefmt"] = "pipe"
    
    return df.to_markdown(**markdown_kwargs)


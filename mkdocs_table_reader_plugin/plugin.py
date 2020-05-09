import os
import re
import pandas as pd
from mkdocs.plugins import BasePlugin
from .safe_eval import parse_argkwarg


def read_csv(*args, **kwargs):
    df = pd.read_csv(*args, **kwargs)
    return df.to_markdown(showindex=False)


def read_table(*args, **kwargs):
    df = pd.read_table(*args, **kwargs)
    return df.to_markdown(showindex=False)


def read_fwf(*args, **kwargs):
    df = pd.read_fwf(*args, **kwargs)
    return df.to_markdown(showindex=False)


def read_excel(*args, **kwargs):
    df = pd.read_excel(*args, **kwargs)
    return df.to_markdown(showindex=False)


READERS = {
    "read_csv": read_csv,
    "read_table": read_table,
    "read_fwf": read_fwf,
    "read_excel": read_excel,
}


class cd:
    """
    Context manager for changing the current working directory
    Credits: https://stackoverflow.com/a/13197763/5525118
    """

    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


class TableReaderPlugin(BasePlugin):
    def on_page_markdown(self, markdown, page, config, files):
        """
        Replace jinja tag {{ read_csv() }} in markdown with markdown table.

        The page_markdown event is called after the page's markdown is loaded
        from file and can be used to alter the Markdown source text.
        The meta- data has been stripped off and is available as page.meta
        at this point.

        https://www.mkdocs.org/user-guide/plugins/#on_page_markdown

        Args:
            markdown (str): Markdown source text of page as string
            page: mkdocs.nav.Page instance
            config: global configuration object
            site_navigation: global navigation object

        Returns:
            str: Markdown source text of page as string
        """

        mkdocs_dir = os.path.dirname(config["config_file_path"])

        for reader, function in READERS.items():

            # Searches for tag like {{ read_csv(..) }}
            # and extract string with arguments (positional and keywords)
            tag_pattern = re.compile(
                "\{\{ %s\((.+)\) \}\}" % reader, flags=re.IGNORECASE
            )

            # If tag not present, do not alter markdown
            result = tag_pattern.search(markdown)
            if not result:
                continue

            # Safely parse the arguments
            argkwarg_string = result.group(1)
            args, kwargs = parse_argkwarg(argkwarg_string)

            # Insert markdown table
            with cd(mkdocs_dir):
                markdown_table = function(*args, **kwargs)
            markdown = tag_pattern.sub(markdown_table, markdown)

        return markdown

import os
import re
import pandas as pd
from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options

from .safe_eval import parse_argkwarg


def read_csv(*args, **kwargs):
    df = pd.read_csv(*args, **kwargs)
    return df.to_markdown(showindex=False, tablefmt="pipe")


def read_table(*args, **kwargs):
    df = pd.read_table(*args, **kwargs)
    return df.to_markdown(showindex=False, tablefmt="pipe")


def read_fwf(*args, **kwargs):
    df = pd.read_fwf(*args, **kwargs)
    return df.to_markdown(showindex=False, tablefmt="pipe")


def read_excel(*args, **kwargs):
    df = pd.read_excel(*args, **kwargs)
    return df.to_markdown(showindex=False, tablefmt="pipe")


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

    config_scheme = (("data_path", config_options.Type(str, default=".")),)

    def on_page_markdown(self, markdown, page, config, files, **kwargs):
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

            # Regex pattern for tags like {{ read_csv(..) }}
            # with a match group to extract the arguments (positional and keywords)
            tag_pattern = re.compile(
                "\{\{ %s\((.+)\) \}\}" % reader, flags=re.IGNORECASE
            )

            matches = re.findall(tag_pattern, markdown)
            for result in matches:

                # Safely parse the arguments
                pd_args, pd_kwargs = parse_argkwarg(result)

                # Make sure the path is relative to "data_path"
                if len(pd_args) > 0:
                    pd_args[0] = os.path.join(self.config.get("data_path"), pd_args[0])
                    file_path = pd_args[0]

                if pd_kwargs.get("filepath_or_buffer"):
                    file_path = pd_kwargs["filepath_or_buffer"]
                    file_path = os.path.join(self.config.get("data_path"), file_path)
                    pd_kwargs["filepath_or_buffer"] = file_path

                # Insert markdown table
                # By replacing first occurance of the regex pattern
                with cd(mkdocs_dir):
                    if not os.path.exists(file_path):
                        raise FileNotFoundError(
                            "[table-reader-plugin]: File does not exist: %s" % file_path
                        )

                    markdown_table = function(*pd_args, **pd_kwargs)

                markdown = tag_pattern.sub(markdown_table, markdown, count=1)

        return markdown

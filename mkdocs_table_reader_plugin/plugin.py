import re
import pandas as pd
from mkdocs.plugins import BasePlugin

def read_csv(*args, **kwargs):
    df = pd.read_csv(*args, **kwargs)
    # todo, make configable?
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

        # Searches for {{ read_csv(..) }}
        # and extracts command
        tag_pattern = re.compile(
            "\{\{ (read_csv\(.+\)) \}\}", 
            flags=re.IGNORECASE
        )
        
        result = tag_pattern.search(markdown)
        if not result:
            return markdown
        
        command = result.group(1)
        if command is not None and command != "":
            markdown_table = eval(command)
        
        return tag_pattern.sub(
            markdown_table,
            markdown
        )

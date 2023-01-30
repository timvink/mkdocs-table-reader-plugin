import os
import re
import logging

from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options
from mkdocs.exceptions import ConfigurationError

from mkdocs_table_reader_plugin.safe_eval import parse_argkwarg
from mkdocs_table_reader_plugin.readers import READERS
from mkdocs_table_reader_plugin.markdown import fix_indentation

logger = logging.getLogger("mkdocs.plugins")

class TableReaderPlugin(BasePlugin):

    config_scheme = (
        ("base_path", config_options.Choice(['docs_dir','config_dir'], default="config_dir")),
        ("data_path", config_options.Type(str, default=".")),
        ("search_page_directory", config_options.Type(bool, default=True)),
        ("allow_missing_files", config_options.Type(bool, default=False)),
    )

    def on_config(self, config, **kwargs):
        """
        See https://www.mkdocs.org/user-guide/plugins/#on_config.

        Args:
            config

        Returns:
            Config
        """
        plugins = [p for p in config.get("plugins")]

        for post_load_plugin in ["macros", "markdownextradata"]:
            if post_load_plugin in plugins:
                if plugins.index("table-reader") > plugins.index(post_load_plugin):
                    raise ConfigurationError(f"[table-reader]: Incompatible plugin order: Define 'table-reader' before '{post_load_plugin}' in your mkdocs.yml.")


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
        # Determine the mkdocs directory
        # We do this during the on_page_markdown() event because other plugins
        # might have changed the directory.
        if self.config.get("base_path") == "config_dir":
            mkdocs_dir = os.path.dirname(os.path.abspath(config["config_file_path"]))
        if self.config.get("base_path") == "docs_dir":
            mkdocs_dir = os.path.abspath(config["docs_dir"])
        
        # Define directories to search for tables
        search_directories = [os.path.join(mkdocs_dir, self.config.get("data_path"))]
        if self.config.get("search_page_directory"):
            search_directories.append(os.path.dirname(page.file.abs_src_path))

        for reader, function in READERS.items():
            
            # Regex pattern for tags like {{ read_csv(..) }}
            # match group 0: to extract any leading whitespace 
            # match group 1: to extract the arguments (positional and keywords)
            tag_pattern = re.compile(
                r"( *)\{\{\s+%s\((.+)\)\s+\}\}" % reader, flags=re.IGNORECASE
            )
            matches = re.findall(tag_pattern, markdown)
            
            for result in matches:

                # Deal with indentation
                # So we can fix inserting tables.
                # f.e. relevant when used inside content tabs
                leading_spaces = result[0]

                # Safely parse the arguments
                pd_args, pd_kwargs = parse_argkwarg(result[1])

                # Extract the filepath,
                # which is the first positional argument
                # or a named argument when there are no positional arguments
                if len(pd_args) > 0:
                    input_file_path = pd_args.pop(0)
                else:
                    input_file_path = pd_kwargs.pop("filepath_or_buffer")

                # Validate if file exists
                search_file_paths = [os.path.join(search_dir, input_file_path) for search_dir in search_directories]
                valid_file_paths = [p for p in search_file_paths if os.path.exists(p)]
                if len(valid_file_paths) == 0:
                    msg = f"[table-reader-plugin]: Cannot find table file '{input_file_path}'. The following directories were searched: {*search_directories,}"
                    if self.config.get("allow_missing_files"):
                        logger.warning(msg)

                        # Add message in markdown
                        updated_tag = fix_indentation(leading_spaces, f"{{{{ Cannot find '{input_file_path}' }}}}")

                        markdown = tag_pattern.sub(updated_tag, markdown, count=1)

                        continue
                    else:
                        raise FileNotFoundError(msg)
                
                # Load the table
                # note we use the first valid file paths,
                # where we first search the 'data_path' and then the page's directory.
                markdown_table = function(valid_file_paths[0], *pd_args, **pd_kwargs)

                markdown_table = fix_indentation(leading_spaces, markdown_table)

                # Insert markdown table
                # By replacing only the first occurance of the regex pattern
                # You might insert multiple CSVs with a single reader like read_csv
                # Because of the replacement, the next occurance will be the first match for .sub() again.
                # This is always why when allow_missing_files=True we replaced the input tag.
                markdown = tag_pattern.sub(markdown_table, markdown, count=1)

        return markdown



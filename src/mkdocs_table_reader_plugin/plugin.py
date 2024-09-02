import re

from mkdocs.config import config_options
from mkdocs.exceptions import ConfigurationError
from mkdocs.plugins import BasePlugin, get_plugin_logger

from mkdocs_table_reader_plugin.markdown import add_indentation, convert_to_md_table, fix_indentation
from mkdocs_table_reader_plugin.readers import MACROS, READERS
from mkdocs_table_reader_plugin.safe_eval import parse_argkwarg

logger = get_plugin_logger("table-reader")


class TableReaderPlugin(BasePlugin):
    config_scheme = (
        ("data_path", config_options.Type(str, default=".")),
        ("allow_missing_files", config_options.Type(bool, default=False)),
        (
            "select_readers",
            config_options.ListOfItems(
                config_options.Choice(list(READERS.keys())),
                default=list(READERS.keys()),
            ),
        ),
    )

    def on_config(self, config, **kwargs):
        """
        See https://www.mkdocs.org/user-guide/plugins/#on_config.

        Args:
            config

        Returns:
            Config
        """
        if "search_page_directory" in self.config:
            logger.warning(
                "[table-reader]: The 'search_page_directory' configuration option is deprecated, it will always be searched. Please remove it from your mkdocs.yml."
            )
        if "base_path" in self.config:
            logger.warning(
                "[table-reader]: The 'base_path' configuration option is deprecated. Both the config_dir and docs_dir will be searched. Please remove it from your mkdocs.yml."
            )

        self.readers = {
            reader: READERS[reader].set_config_context(
                mkdocs_config=config, plugin_config=self.config
            )
            for reader in self.config.get("select_readers")
            if reader in self.config.get("select_readers", [])
        }

        plugins = [p for p in config.get("plugins")]

        # Plugins required before table-reader
        for post_load_plugin in ["markdownextradata"]:
            if post_load_plugin in plugins:
                if plugins.index("table-reader") > plugins.index(post_load_plugin):
                    raise ConfigurationError(
                        f"[table-reader]: Incompatible plugin order: Define 'table-reader' before '{post_load_plugin}' in your mkdocs.yml."
                    )

        # Plugins required after table-reader
        for post_load_plugin in ["macros"]:
            if post_load_plugin in plugins:
                if plugins.index("table-reader") < plugins.index(post_load_plugin):
                    raise ConfigurationError(
                        f"[table-reader]: Incompatible plugin order: Define 'table-reader' after '{post_load_plugin}' in your mkdocs.yml."
                    )

        if "macros" in config.plugins:
            self.macros = {
                macro: MACROS[macro].set_config_context(
                    mkdocs_config=config, plugin_config=self.config
                )
                for macro in MACROS
            }
            self.filters = {
                "add_indentation": add_indentation,
                "convert_to_md_table": convert_to_md_table,
            }
            config.plugins["macros"].macros.update(self.macros)
            config.plugins["macros"].variables["macros"].update(self.macros)
            config.plugins["macros"].env.globals.update(self.macros)

            config.plugins["macros"].filters.update(self.filters)
            config.plugins["macros"].variables["filters"].update(self.filters)
            config.plugins["macros"].env.filters.update(self.filters)

            self.external_jinja_engine = True
        else:
            self.external_jinja_engine = False

    def on_pre_page(self, page, config, **kwargs):
        """
        See https://www.mkdocs.org/dev-guide/plugins/#on_pre_page.

        Args:
            page: mkdocs.nav.Page instance
            config: global configuration object

        Returns:
            Page
        """
        # store the current page in the plugin config
        # because the readers have access to the plugin config, they can know where the current page is
        # this way, they can check that directory too
        self.config._current_page = page.file.abs_src_path
        return page

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
        if self.external_jinja_engine:
            return markdown

        for reader in self.readers:
            function = self.readers[reader]
            # Regex pattern for tags like {{ read_csv(..) }}
            # match group 0: to extract any leading whitespace
            # match group 1: to extract the arguments (positional and keywords)
            tag_pattern = re.compile(
                r"( *)\{\{\s+%s\((.+)\)\s+\}\}" % reader, flags=re.IGNORECASE # noqa: UP031
            )
            matches = re.findall(tag_pattern, markdown)

            for result in matches:
                # Deal with indentation
                # So we can fix inserting tables.
                # f.e. relevant when used inside content tabs
                leading_spaces = result[0]

                # Safely parse the arguments
                pd_args, pd_kwargs = parse_argkwarg(result[1])

                # Load the table
                markdown_table = function(*pd_args, **pd_kwargs)

                # Insert markdown table
                # By replacing only the first occurrence of the regex pattern
                # You might insert multiple CSVs with a single reader like read_csv
                # Because of the replacement, the next occurrence will be the first match for .sub() again.
                # This is always why when allow_missing_files=True we replaced the input tag.
                markdown_table = fix_indentation(leading_spaces=leading_spaces, text=markdown_table)
                markdown = tag_pattern.sub(markdown_table, markdown, count=1)

        return markdown

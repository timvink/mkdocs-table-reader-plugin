"""
Note that pytest offers a `tmp_path`. 
You can reproduce locally with

```python
%load_ext autoreload
%autoreload 2
import os
import tempfile
import shutil
from pathlib import Path
tmp_path = Path(tempfile.gettempdir()) / 'pytest-table-builder'
if os.path.exists(tmp_path):
    shutil.rmtree(tmp_path)
os.mkdir(tmp_path)
```
"""

import logging
import os
import re
import shutil
import sys

import pandas as pd
import pytest
from click.testing import CliRunner
from mkdocs.__main__ import build_command


def setup_clean_mkdocs_folder(mkdocs_yml_path, output_path):
    """
    Sets up a clean mkdocs directory
    
    outputpath/testproject
    ├── docs/
    └── mkdocs.yml
    
    Args:
        mkdocs_yml_path (Path): Path of mkdocs.yml file to use
        output_path (Path): Path of folder in which to create mkdocs project
        
    Returns:
        testproject_path (Path): Path to test project
    """

    testproject_path = output_path / "testproject"

    # Create empty 'testproject' folder
    if os.path.exists(testproject_path):
        logging.warning(
            """This command does not work on windows. 
        Refactor your test to use setup_clean_mkdocs_folder() only once"""
        )
        shutil.rmtree(testproject_path)

    # Copy correct mkdocs.yml file and our test 'docs/'
    shutil.copytree(
        os.path.join(os.path.dirname(mkdocs_yml_path), "docs"),
        testproject_path / "docs",
    )
    if os.path.exists(os.path.join(os.path.dirname(mkdocs_yml_path), "assets")):
        shutil.copytree(
            os.path.join(os.path.dirname(mkdocs_yml_path), "assets"),
            testproject_path / "assets",
        )
    shutil.copyfile(mkdocs_yml_path, testproject_path / "mkdocs.yml")

    return testproject_path


def build_docs_setup(testproject_path):
    """
    Runs the `mkdocs build` command
    
    Args:
        testproject_path (Path): Path to test project
    
    Returns:
        command: Object with results of command
    """

    cwd = os.getcwd()
    os.chdir(testproject_path)

    try:
        run = CliRunner().invoke(build_command)
        os.chdir(cwd)
        return run
    except:
        os.chdir(cwd)
        raise



def test_table_output(tmp_path):

    tmp_proj = setup_clean_mkdocs_folder(
        "tests/fixtures/basic_setup/mkdocs.yml", tmp_path
    )

    result = build_docs_setup(tmp_proj)
    assert result.exit_code == 0, "'mkdocs build' command failed"

    index_file = tmp_proj / "site/index.html"
    assert index_file.exists(), f"{index_file} does not exist"

    # Make sure with markdown tag has the output
    page_with_tag = tmp_proj / "site/page_read_csv.html"
    contents = page_with_tag.read_text()
    assert re.search(r"531456", contents)

    # Make sure with markdown tag has the output
    page_with_tag = tmp_proj / "site/page_read_txt.html"
    contents = page_with_tag.read_text()
    assert re.search(r"531456", contents)

    # Make sure with markdown tag has the output
    page_with_tag = tmp_proj / "site/page_read_excel.html"
    contents = page_with_tag.read_text()
    assert re.search(r"531456", contents)

    # Make sure with markdown tag has the output
    page_with_tag = tmp_proj / "site/page_read_fwf.html"
    contents = page_with_tag.read_text()
    assert re.search(r"35000", contents)
    assert re.search(r"Audi A4", contents)

    # Make sure with markdown tag has the output
    page_with_tag = tmp_proj / "site/page_read_yaml.html"
    contents = page_with_tag.read_text()
    assert re.search(r"531456", contents)
    assert re.search(r"table1", contents)

    # Make sure with markdown tag has the output
    page_with_tag = tmp_proj / "site/page_read_json.html"
    contents = page_with_tag.read_text()
    assert re.search(r"1234json", contents)

    # Make sure multiple tags are supported
    page_with_tag = tmp_proj / "site/page_read_two_csv.html"
    contents = page_with_tag.read_text()
    assert re.search(r"table1", contents)
    assert re.search(r"table2", contents)
    # Two tags on the same line are two tables, and the text between them survives
    assert re.search(r"and that is that", contents)
    assert len(re.findall(r"table1", contents)) == 2
    assert len(re.findall(r"table2", contents)) == 2


def test_compatibility_macros_plugin(tmp_path):

    tmp_proj = setup_clean_mkdocs_folder(
        "tests/fixtures/basic_setup/mkdocs_w_macros_wrong_order.yml", tmp_path
    )

    result = build_docs_setup(tmp_proj)
    assert result.exit_code == 1, "'mkdocs build' command should have failed"

    # Make sure correct error is raised
    assert (
        "[table-reader]: Incompatible plugin order:"
        in result.output
    )

    # With correct order, no error
    tmp_proj = setup_clean_mkdocs_folder(
        "tests/fixtures/basic_setup/mkdocs_w_macros.yml", tmp_path
    )

    result = build_docs_setup(tmp_proj)
    assert result.exit_code == 0, "'mkdocs build' command should have succeeded"

def test_compatibility_markdownextradata(tmp_path):

    tmp_proj = setup_clean_mkdocs_folder(
        "tests/fixtures/markdownextradata/mkdocs.yml", tmp_path
    )

    result = build_docs_setup(tmp_proj)
    assert result.exit_code == 0, "'mkdocs build' command failed"

    index_file = tmp_proj / "site/index.html"
    assert index_file.exists(), f"{index_file} does not exist"

    # Make sure with markdown tag has the output
    page_with_tag = tmp_proj / "site/index.html"
    contents = page_with_tag.read_text()
    # Make sure the table is inserted
    assert re.search(r"531456", contents)
    # Make sure the extradata 'web' is inserted
    assert re.search(r"www.example.com", contents)

    tmp_proj = setup_clean_mkdocs_folder(
        "tests/fixtures/markdownextradata/mkdocs_w_markdownextradata_wrong_order.yml", tmp_path
    )

    result = build_docs_setup(tmp_proj)
    assert result.exit_code == 1, "'mkdocs build' command should have failed"

    # Make sure correct error is raised
    assert (
        "[table-reader]: Incompatible plugin order:"
        in result.output
    )

    # With correct order, no error
    tmp_proj = setup_clean_mkdocs_folder(
        "tests/fixtures/markdownextradata/mkdocs_w_markdownextradata.yml", tmp_path
    )

    result = build_docs_setup(tmp_proj)
    assert result.exit_code == 0, "'mkdocs build' command should have succeeded"


def test_search_page_directory(tmp_path):

    tmp_proj = setup_clean_mkdocs_folder(
        "tests/fixtures/search_page_directory/mkdocs.yml", tmp_path
    )

    result = build_docs_setup(tmp_proj)
    assert result.exit_code == 0, "'mkdocs build' command failed"

    # Make sure the basic_table.csv is inserted
    page_with_tag = tmp_proj / "site/folder/page2.html"
    contents = page_with_tag.read_text()
    assert re.search(r"531456", contents)

def test_relative_path(tmp_path):
    """
    A project where we specify a path relative to the markdown.
    """

    tmp_proj = setup_clean_mkdocs_folder(
        "tests/fixtures/relative_path/mkdocs.yml", tmp_path
    )

    result = build_docs_setup(tmp_proj)
    assert result.exit_code == 0, "'mkdocs build' command failed"

    # Make sure the basic_table.csv is inserted
    page_with_tag = tmp_proj / "site/folder/page2.html"
    contents = page_with_tag.read_text()
    assert re.search(r"531456", contents)


def test_raw_cotent(tmp_path):
    """
    A project where we insert raw content directly.
    """

    tmp_proj = setup_clean_mkdocs_folder(
        "tests/fixtures/raw_content/mkdocs.yml", tmp_path
    )

    result = build_docs_setup(tmp_proj)
    assert result.exit_code == 0, "'mkdocs build' command failed"

    # Make sure the basic_table.csv is inserted
    page_with_tag = tmp_proj / "site/folder/page2.html"
    contents = page_with_tag.read_text()
    assert re.search(r"\$1600", contents)


def test_datapath_1(tmp_path):

    tmp_proj = setup_clean_mkdocs_folder(
        "tests/fixtures/datapathproject/mkdocs.yml", tmp_path
    )

    result = build_docs_setup(tmp_proj)
    assert result.exit_code == 0, "'mkdocs build' command failed"

    # Make sure the basic_table.csv is inserted
    page_with_tag = tmp_proj / "site/index.html"
    contents = page_with_tag.read_text()
    assert re.search(r"531456", contents)

    # Make sure the basic_table2.csv is inserted
    page_with_tag = tmp_proj / "site/page2.html"
    contents = page_with_tag.read_text()
    assert re.search(r"539956", contents)


def test_datapath_trailing(tmp_path):

    tmp_proj = setup_clean_mkdocs_folder(
        "tests/fixtures/datapathproject/mkdocs_trailingslash.yml", tmp_path
    )

    result = build_docs_setup(tmp_proj)
    assert result.exit_code == 0, "'mkdocs build' command failed"

    # Make sure the basic_table.csv is inserted
    page_with_tag = tmp_proj / "site/index.html"
    contents = page_with_tag.read_text()
    assert re.search(r"531456", contents)

    # Make sure the basic_table2.csv is inserted
    page_with_tag = tmp_proj / "site/page2.html"
    contents = page_with_tag.read_text()
    assert re.search(r"539956", contents)


def test_datapath_with_spaces(tmp_path):

    tmp_proj = setup_clean_mkdocs_folder(
        "tests/fixtures/data_path_with_space/mkdocs.yml", tmp_path
    )

    result = build_docs_setup(tmp_proj)
    assert result.exit_code == 0, "'mkdocs build' command failed"

    # Make sure the basic_table.csv is inserted
    page_with_tag = tmp_proj / "site/index.html"
    contents = page_with_tag.read_text()
    assert re.search(r"531456", contents)


def test_tablepath_with_spaces(tmp_path):

    tmp_proj = setup_clean_mkdocs_folder(
        "tests/fixtures/table_path_with_space/mkdocs.yml", tmp_path
    )

    result = build_docs_setup(tmp_proj)
    assert result.exit_code == 0, "'mkdocs build' command failed"

    # Make sure the basic_table.csv is inserted
    page_with_tag = tmp_proj / "site/index.html"
    contents = page_with_tag.read_text()
    assert re.search(r"531456", contents)


def test_using_docs_dir(tmp_path):

    tmp_proj = setup_clean_mkdocs_folder(
        "tests/fixtures/using_docs_dir/mkdocs.yml", tmp_path
    )

    result = build_docs_setup(tmp_proj)
    assert result.exit_code == 0, "'mkdocs build' command failed"

    # Make sure the basic_table.csv is inserted
    page_with_tag = tmp_proj / "site/index.html"
    contents = page_with_tag.read_text()
    assert re.search(r"531456", contents)

def test_wrong_path(tmp_path):

    tmp_proj = setup_clean_mkdocs_folder(
        "tests/fixtures/wrongpath/mkdocs.yml", tmp_path
    )

    result = build_docs_setup(tmp_proj)
    assert result.exit_code == 1, "'mkdocs build' command succeeded but should have failed"
    # Assert on the raised exception rather than on the captured log output.
    # mkdocs logs the error and then re-raises it, and whether that log record
    # makes it into result.output turns out to be flaky on windows.
    assert isinstance(result.exception, FileNotFoundError)
    assert "[table-reader-plugin]: Cannot find table file" in str(result.exception)
    assert "non_existing_table.csv" in str(result.exception)


def test_mixed_quotation_marks(tmp_path):
    tmp_proj = setup_clean_mkdocs_folder(
        "tests/fixtures/mixed_quotation_marks/mkdocs.yml", tmp_path
    )
    result = build_docs_setup(tmp_proj)
    assert result.exit_code == 0, "'mkdocs build' command failed"

    # Make sure the file.csv is inserted
    page_with_tag = tmp_proj / "site/index.html"
    contents = page_with_tag.read_text()
    assert re.search(r"56", contents)

def test_csv_with_no_string_headers(tmp_path):
    tmp_proj = setup_clean_mkdocs_folder(
        "tests/fixtures/nonstringheaders/mkdocs.yml", tmp_path
    )
    result = build_docs_setup(tmp_proj)
    assert result.exit_code == 0, "'mkdocs build' command failed"

    # Make sure the file.csv is inserted
    page_with_tag = tmp_proj / "site/index.html"
    contents = page_with_tag.read_text()
    assert re.search(r"4242", contents)

def test_macros_jinja2_syntax(tmp_path):
    tmp_proj = setup_clean_mkdocs_folder(
        "tests/fixtures/jinja/mkdocs.yml", tmp_path
    )
    result = build_docs_setup(tmp_proj)
    assert result.exit_code == 0, "'mkdocs build' command failed"

    # Make sure the file.csv is inserted
    page_with_tag = tmp_proj / "site/index.html"
    contents = page_with_tag.read_text()
    assert re.search(r"531456", contents)


def test_non_utf8_encoding(tmp_path):
    """
    A project where files are not UTF-8 encoded, and 'encoding' is specified.
    """

    tmp_proj = setup_clean_mkdocs_folder(
        "tests/fixtures/encoding/mkdocs.yml", tmp_path
    )

    result = build_docs_setup(tmp_proj)
    assert result.exit_code == 0, "'mkdocs build' command failed"

    page_with_tag = tmp_proj / "site/index.html"
    contents = page_with_tag.read_text(encoding="utf-8")
    # read_yaml() inserted the cp1251 encoded yaml file
    assert re.search(r"531456", contents)
    assert re.search(r"Хлеб", contents)
    # read_raw() inserted the cp1251 encoded markdown file
    assert re.search(r"539956", contents)
    assert re.search(r"Сыр", contents)


def test_csv_with_multiline_cells(tmp_path):
    """
    A CSV with a quoted, multiline cell should render as a single table row.

    See https://github.com/timvink/mkdocs-table-reader-plugin/issues/83
    """

    tmp_proj = setup_clean_mkdocs_folder(
        "tests/fixtures/csv_multiline/mkdocs.yml", tmp_path
    )

    result = build_docs_setup(tmp_proj)
    assert result.exit_code == 0, "'mkdocs build' command failed"

    page_with_tag = tmp_proj / "site/index.html"
    contents = page_with_tag.read_text()

    # The multiline cell is kept together on one row, separated by <br>
    assert re.search(
        r"Sometimes the cell text is quoted\.<br><br>But not always", contents
    )
    # Both CSV records became a table row, and no newline split them up
    table = re.search(r"<table>.*?</table>", contents, flags=re.DOTALL)
    assert table is not None, "no table was inserted"
    assert len(re.findall(r"<tr>", table.group())) == 3


def test_pandas_readers(tmp_path):
    """
    A project that uses the readers for the other formats supported by pandas.
    """

    tmp_proj = setup_clean_mkdocs_folder(
        "tests/fixtures/pandas_readers/mkdocs.yml", tmp_path
    )

    result = build_docs_setup(tmp_proj)
    assert result.exit_code == 0, "'mkdocs build' command failed"

    contents = (tmp_proj / "site/index.html").read_text()
    for reader in ["parquet", "stata", "sas", "xml"]:
        assert re.search(f"{reader}_table", contents), f"read_{reader}() did not insert the table"
    assert contents.count("531456") == 4


@pytest.mark.skipif(
    sys.platform.startswith("win"),
    reason="pd.read_orc() cannot find the IANA time zone database on windows",
)
def test_read_orc(tmp_path):
    """
    A project that uses read_orc().
    """

    tmp_proj = setup_clean_mkdocs_folder(
        "tests/fixtures/pandas_readers_orc/mkdocs.yml", tmp_path
    )

    result = build_docs_setup(tmp_proj)
    assert result.exit_code == 0, "'mkdocs build' command failed"

    contents = (tmp_proj / "site/index.html").read_text()
    assert re.search(r"orc_table", contents)
    assert re.search(r"531456", contents)


def test_read_html(tmp_path):
    """
    A project that uses read_html(), which returns all tables it finds.
    """
    pytest.importorskip("lxml")

    tmp_proj = setup_clean_mkdocs_folder(
        "tests/fixtures/pandas_readers_html/mkdocs.yml", tmp_path
    )

    result = build_docs_setup(tmp_proj)
    assert result.exit_code == 0, "'mkdocs build' command failed"

    contents = (tmp_proj / "site/index.html").read_text()
    # Without 'match', the first table in the file is inserted
    assert re.search(r"html_table", contents)
    # With 'match', the table that matches is inserted
    assert re.search(r"second_html_table", contents)
    assert re.search(r"539956", contents)
    # read_xml() with the default (lxml) parser
    assert re.search(r"xml_table", contents)


def test_read_spss(tmp_path):
    """
    A project that uses read_spss(), which requires pyreadstat.
    """
    pytest.importorskip("pyreadstat")

    tmp_proj = setup_clean_mkdocs_folder(
        "tests/fixtures/pandas_readers_spss/mkdocs.yml", tmp_path
    )

    result = build_docs_setup(tmp_proj)
    assert result.exit_code == 0, "'mkdocs build' command failed"

    contents = (tmp_proj / "site/index.html").read_text()
    assert re.search(r"spss_table", contents)
    assert re.search(r"531456", contents)


def test_read_hdf(tmp_path):
    """
    A project that uses read_hdf(), which requires pytables.
    """
    pytest.importorskip("tables")

    tmp_proj = setup_clean_mkdocs_folder(
        "tests/fixtures/pandas_readers_hdf/mkdocs.yml", tmp_path
    )
    table_path = tmp_proj / "assets/tables"
    table_path.mkdir(parents=True)
    # a pd.Series, to make sure read_hdf() can also insert those
    pd.Series([531456, 80], name="hdf_table").to_hdf(table_path / "table.h5", key="table", mode="w")

    result = build_docs_setup(tmp_proj)
    assert result.exit_code == 0, "'mkdocs build' command failed"

    contents = (tmp_proj / "site/index.html").read_text()
    assert re.search(r"hdf_table", contents)
    assert re.search(r"531456", contents)


def test_backslashes_in_tables(tmp_path):
    """
    A project with table values that look like a regex replacement.
    """

    tmp_proj = setup_clean_mkdocs_folder(
        "tests/fixtures/backslashes/mkdocs.yml", tmp_path
    )

    result = build_docs_setup(tmp_proj)
    assert result.exit_code == 0, "'mkdocs build' command failed"

    contents = (tmp_proj / "site/index.html").read_text()
    # values are inserted as they are, and not expanded as a regex replacement
    assert r"C:\1 path" in contents
    assert r"hi\nthere" in contents


def test_allow_missing_files(tmp_path):
    """
    With 'allow_missing_files', a missing table is a warning instead of an error.
    """

    tmp_proj = setup_clean_mkdocs_folder(
        "tests/fixtures/wrongpath/mkdocs_allow_missing.yml", tmp_path
    )

    result = build_docs_setup(tmp_proj)
    assert result.exit_code == 0, "'mkdocs build' command failed"

    contents = (tmp_proj / "site/index.html").read_text()
    # The tag is replaced with a note about the missing file
    assert "{{ Cannot find 'non_existing_table.csv' }}" in contents
    # And the tables that do exist are still inserted
    assert re.search(r"531456", contents)


def test_select_readers(tmp_path):
    """
    Only the selected readers replace their tag.
    """

    tmp_proj = setup_clean_mkdocs_folder(
        "tests/fixtures/select_readers/mkdocs.yml", tmp_path
    )

    result = build_docs_setup(tmp_proj)
    assert result.exit_code == 0, "'mkdocs build' command failed"

    contents = (tmp_proj / "site/index.html").read_text()
    # read_csv() is selected, so its table is inserted
    assert re.search(r"531456", contents)
    # read_json() is not, so its tag is left alone
    assert '{{ read_json("data.json") }}' in contents
    assert "1234json" not in contents


def test_select_readers_unknown(tmp_path):
    """
    A reader that does not exist is a configuration error.
    """

    tmp_proj = setup_clean_mkdocs_folder(
        "tests/fixtures/select_readers/mkdocs_unknown_reader.yml", tmp_path
    )

    result = build_docs_setup(tmp_proj)
    assert result.exit_code == 1, "'mkdocs build' command should have failed"
    assert "select_readers" in result.output
    assert "read_avro" in result.output


def test_indentation(tmp_path):
    """
    A table keeps the indentation of its tag, so it can go inside components
    that rely on indentation, like admonitions and content tabs.
    """

    tmp_proj = setup_clean_mkdocs_folder(
        "tests/fixtures/indentation/mkdocs.yml", tmp_path
    )

    result = build_docs_setup(tmp_proj)
    assert result.exit_code == 0, "'mkdocs build' command failed"

    contents = (tmp_proj / "site/index.html").read_text()
    # Every tag was replaced
    assert "read_csv" not in contents
    assert len(re.findall(r"<table>", contents)) == 3
    # The indented tables ended up inside the component, instead of after it
    assert re.search(
        r'<div class="admonition note">\s*<p class="admonition-title">A note</p>\s*<table>',
        contents,
    ), "the table was not inserted inside the admonition"
    assert re.search(
        r'<div class="tabbed-block">\s*<table>', contents
    ), "the table was not inserted inside the content tab"


def test_tags_in_inserted_content(tmp_path):
    """
    Inserted content is not searched for tags itself.

    Every tag is replaced in a single pass, so a table or a raw file that
    contains something that looks like a tag is inserted as-is.
    """

    tmp_proj = setup_clean_mkdocs_folder(
        "tests/fixtures/raw_content/mkdocs.yml", tmp_path
    )

    result = build_docs_setup(tmp_proj)
    assert result.exit_code == 0, "'mkdocs build' command failed"

    contents = (tmp_proj / "site/index.html").read_text()
    # The raw file was inserted
    assert "This file documents a reader tag" in contents
    # ..including the tag it contains, which was not read (the file does not exist)
    assert '{{ read_csv("no_such_table.csv") }}' in contents


def test_malformed_tags(tmp_path):
    """
    A tag that is not formatted correctly is left alone, instead of failing the build.
    """

    tmp_proj = setup_clean_mkdocs_folder(
        "tests/fixtures/basic_setup/mkdocs.yml", tmp_path
    )

    result = build_docs_setup(tmp_proj)
    assert result.exit_code == 0, "'mkdocs build' command failed"

    contents = (tmp_proj / "site/bad_tags.html").read_text()
    for tag in [
        "{{ read_csv }}",  # no call
        "{{ read_csv() }}",  # no arguments
        "{{read_csv('path')}}",  # no spaces inside the braces
        "{{read_csv('path') }}",
        "{{ read_csv('path')}}",
    ]:
        assert tag in contents, f"the malformed tag {tag} was not left alone"

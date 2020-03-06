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

import re
import os
import shutil
import logging
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

    testproject_path = output_path / 'testproject'
    
    # Create empty 'testproject' folder    
    if os.path.exists(testproject_path):
        logging.warning("""This command does not work on windows. 
        Refactor your test to use setup_clean_mkdocs_folder() only once""")
        shutil.rmtree(testproject_path)

    # Copy correct mkdocs.yml file and our test 'docs/'        
    shutil.copytree('tests/basic_setup/docs', testproject_path / 'docs')
    shutil.copytree('tests/basic_setup/assets', testproject_path / 'assets')
    shutil.copyfile(mkdocs_yml_path, testproject_path / 'mkdocs.yml')
    
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
    
    tmp_proj = setup_clean_mkdocs_folder('tests/basic_setup/mkdocs.yml', tmp_path)
    
    result = build_docs_setup(tmp_proj)
    assert result.exit_code == 0, "'mkdocs build' command failed"
    
    index_file = tmp_proj / 'site/index.html'
    assert index_file.exists(),  f"{index_file} does not exist"
    
    # Make sure with markdown tag has the output
    page_with_tag = tmp_proj / 'site/page_with_tag/index.html'
    contents = page_with_tag.read_text()
    assert re.search(r"531456", contents)
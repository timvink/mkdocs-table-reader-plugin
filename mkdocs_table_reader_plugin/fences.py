from pymdownx.superfences import _escape
from pymdownx.superfences import SuperFencesException

from mkdocs.exceptions import PluginError
from mkdocs_table_reader_plugin.readers import READERS

def fence_tablereader(source, language, class_name, options, md, **kwargs):
    """
    Inspired by https://github.com/facelessuser/pymdown-extensions/blob/8ee5b5caec8f9373e025f50064585fb9d9b71f86/pymdownx/superfences.py#L146
    """  # noqa
    # if not some_validation_function(source):
    #     raise SuperFencesException from PluginError(f"Your vegalite syntax is not valid JSON. Fix:\n\n{source}")

    classes = kwargs["classes"]
    id_value = kwargs["id_value"]
    attrs = kwargs["attrs"]
    
    txt_input = str(_escape(source))
    lines = txt_input.split('\n')
    user_input = {}

    for line in lines:
        key, value = line.split(':', 1)
        key = key.strip()
        value = value.strip()
        user_input[key] = value

    breakpoint()
    return READERS[user_input['reader']](user_input['filepath'])


    # The problem is that this function returns markdown instead of HTML.
    # A possible solution might to to use pandas .to_html() instead of .to_markdown()
    # this requires adapting our READERS functions though. 


"""
This module exists to prevent having to use `eval()`.

`ast.literal_eval()` is not a drop-in replacement however, the function `safe_eval.safe_eval()` will catch some edge cases.

A downside of literal_eval() is that is cannot parse
special characters like newlines (\r\t or \n). We need those kind of characters because pandas.read_csv() accepts 
a parameter 'sep' that could contain all sorts of regex.

As an example, if we have this in our markdown file:

```markdown
{{ read_csv('my/path/table.csv', sep = '\t\n') }}
```

We use regex to first extract the argkwarg string:

"'my/path/table.csv', sep = '\t\n'"

And we then need to parse that into args and kwargs:

>>> args
['my/path/table.csv']
>>> kwargs
{'sep' : '\t\n'}

So we can finally use those to safely run pd.read_csv(*args, **kwargs)

"""

import re
from ast import literal_eval


def safe_eval(string):
    """
    A downside of literal_eval() is that is cannot parse
    special characters like newlines (\r\t or \n).
    
    We need this because pandas.read_csv() accepts 
    a parameter 'sep' that could contain all sorts of regex.

    Args:
        string (str): string to parse to literal python

    Returns:
        str: The parsed literal python structure 
    """
    if "\n" in string or "\\" in string or "\r" in string:
        # remove quotes
        string = string.replace("'", "")
        string = string.replace('"', "")
        return string
    else:
        return literal_eval(string)


def parse_argkwarg(string: str):
    """
    Parses a string to detect both args and kwargs.
    
    Adapted code from 
    https://stackoverflow.com/questions/9305387/string-of-kwargs-to-kwargs

    Args:
        string (str): string with positional and keyword arguments
        
    Returns:
        args[List], kwargs[Dict]
    """

    argkwargs = re.split(r"(?<!\=)(?:,{1} )(?!\=)", string)

    args = []
    kwargs = []

    for i in argkwargs:
        i = i.strip()
        if "=" in i:
            kwargs.append(i)
        else:
            if len(kwargs) != 0:
                raise AssertionError(
                    "[table-reader-plugin] Make sure the python in your reader tag is correct: Positional arguments follow keyword arguments in '%s'"
                    % string
                )
            args.append(literal_eval(i))

    # kwargs as dict
    kwargs = [re.split(" ?= ?", x) for x in kwargs]
    kwargs = dict([(x[0], safe_eval(x[1])) for x in kwargs])

    return args, kwargs

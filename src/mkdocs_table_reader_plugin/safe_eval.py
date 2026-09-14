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


def scan(input_str: str):
    """
    Walk through a string, keeping track of what is nested inside something else.

    A character is top level when it is not inside quotes and not inside
    brackets, braces or parentheses. That is what tells a separator between two
    arguments apart from the same character inside a value, as in
    `read_csv('a=b.csv', dtype={'a': 'str', 'b': 'int'})`.

    Args:
        input_str (str): string with positional and keyword arguments

    Yields:
        (int, str, bool): position, character, and whether it is top level
    """
    in_quotes = False
    quote_char = ""
    depth = 0

    for position, char in enumerate(input_str):
        if in_quotes:
            if char == quote_char:
                in_quotes = False
                quote_char = ""
        elif char in "\"'":
            in_quotes = True
            quote_char = char
        elif char in "([{":
            depth += 1
        elif char in ")]}":
            depth -= 1
        else:
            yield position, char, depth == 0
            continue

        yield position, char, False


def split_top_level(input_str: str, separator: str) -> list:
    """
    Split a string on a separator, ignoring separators nested inside a value.

    Args:
        input_str (str): string with positional and keyword arguments
        separator (str): single character to split on

    Returns:
        list: the stripped segments between the separators
    """
    segments = []
    start = 0

    for position, char, top_level in scan(input_str):
        if char == separator and top_level:
            segments.append(input_str[start:position].strip())
            start = position + 1

    segments.append(input_str[start:].strip())
    return segments


def find_top_level(input_str: str, separator: str) -> int:
    """
    Find the first separator that is not nested inside a value.

    Args:
        input_str (str): a single positional or keyword argument
        separator (str): single character to look for

    Returns:
        int: the position of the separator, or -1 when there is none
    """
    for position, char, top_level in scan(input_str):
        if char == separator and top_level:
            return position

    return -1


def parse_argkwarg(input_str: str):
    """
    Parses a string to detect both args and kwargs.

    Args:
        input_str (str): string with positional and keyword arguments

    Returns:
        args[List], kwargs[Dict]
    """
    args = []
    kwargs = {}

    for segment in split_top_level(input_str, ","):
        position = find_top_level(segment, "=")

        if position == -1:
            if kwargs:
                raise AssertionError(
                    f"[table-reader-plugin] Make sure the python in your reader tag is correct: Positional arguments follow keyword arguments in '{input_str}'"
                )
            args.append(literal_eval(segment))
        else:
            kwargs[segment[:position].strip()] = safe_eval(segment[position + 1 :].strip())

    return args, kwargs

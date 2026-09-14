import os
from inspect import signature


def get_keywords(*funcs):
    """Collect the keyword arguments accepted by one or more functions."""
    return [
        p.name
        for func in funcs
        for p in signature(func).parameters.values()
        if p.kind == p.POSITIONAL_OR_KEYWORD or p.kind == p.KEYWORD_ONLY
    ]


def kwargs_in_func(keywordargs, *funcs):
    keywords = get_keywords(*funcs)
    return {k: v for k, v in keywordargs.items() if k in keywords}


def kwargs_not_in_func(keywordargs, *funcs):
    keywords = get_keywords(*funcs)
    return {k: v for k, v in keywordargs.items() if k not in keywords}


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

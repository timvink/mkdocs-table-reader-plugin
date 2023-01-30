import os
from inspect import signature 

def get_keywords(func):
    return [p.name for p in signature(func).parameters.values() if p.kind == p.POSITIONAL_OR_KEYWORD or p.kind == p.KEYWORD_ONLY]

def kwargs_in_func(keywordargs, func):
    return dict({(k,v) for k, v in keywordargs.items() if k in get_keywords(func)})

def kwargs_not_in_func(keywordargs, func):
    return dict({(k,v) for k, v in keywordargs.items() if k not in get_keywords(func)})


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


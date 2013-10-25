"""
uhdl.utils
~~~~~~~~~~

Utility functions(unrelated to hardware desription) used within uhdl.
"""

import contextlib
import collections
import os
from functools import wraps


@contextlib.contextmanager
def cd(path):
    """Context manager which changes the current working directory

    Args:
        path(str): path to change directory to.

    Usage:
        .. code-block:: python

            with cd('path/to/somewhere'):
                #do something..

    """
    curdir = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(curdir)


class classproperty(object):
    """Decorator which allows read only class properties"""

    def __init__(self,  fget):
        self.fget = fget

    def __get__(self,  owner_self,  owner_cls):
        return self.fget(owner_cls)


def flatten(*args):
    """Flattens arbitrarily nested iterators(Except strings)

    Args:
        *args: objects and iterables.

    Returns:
        list of all objects.
    """
    l = []
    for arg in args:
        if isinstance(arg, collections.Iterable) and not isinstance(arg, str):
            for item in arg:
                l.extend(flatten(item))
        else:
            l.append(arg)
    return l


def memoize(func):
    cache = {}

    @wraps(func)
    def memoized(*args):
        if args in cache:
            result = cache[args]
        else:
            result = func(*args)
            cache[args] = result
        return result
    return memoized

"""
uhdl.utils
~~~~~~~~~~

This module provides utility functions that are used within uhdl that are also
useful outside.

"""

import contextlib
import collections
import os


def create(n, constructor, *args, **kwargs):
    """Returns a list of n instances of constructor(*args, **kwargs)"""
    return [constructor(*args, **kwargs) for _ in range(n)]


@contextlib.contextmanager
def cd(path):
    curdir = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(curdir)



class classproperty(object):

    def __init__(self,  fget):
        self.fget = fget

    def __get__(self,  owner_self,  owner_cls):
        return self.fget(owner_cls)


def flatten(*args):
    l = []
    for arg in args:
        if isinstance(arg, collections.Iterable) and not isinstance(arg, str):
            for item in arg:
                l.extend(flatten(item))
        else:
            l.append(arg)
    return l

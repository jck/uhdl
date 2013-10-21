"""
uhdl.utils
~~~~~~~~~~

This module provides utility functions that are used within uhdl that are also
useful outside.

"""


def create(n, constructor, *args, **kwargs):
    """Returns a list of n instances of constructor(*args, **kwargs)"""
    return [constructor(*args, **kwargs) for _ in range(n)]

"""
uhdl.constructors
~~~~~~~~~~~~~

This module provides the core uhdl constructors.
"""
import random

from myhdl import intbv, Signal

from ._compat import integer_types

def randbits(n):
    return intbv(val=random.getrandbits(n))[n:]

def all_none(*lst):
    return all(x is None for x in lst)


def is_int(x):
    return not isinstance(x, bool) and isinstance(x, integer_types)


def Sig(val=None, w=None, min=None, max=None):
    if all_none(w, min, max):
        if is_int(val):
            val = intbv(val)
        return Signal(val)

    min_max = not all_none(min, max)
    explicit_width = w is not None
    if explicit_width and min_max:
        raise ValueError("Only one of width or min/max must be provided")

    if not is_int(val) and val is not None:
        raise TypeError('Specifying width is supported only for int values')

    if explicit_width:
        val = intbv(val or 0)[w:]
    elif min_max:
        if None in (min, max):
            raise ValueError("Both min and max must be provided")
        val = intbv(val=val or min, min=min, max=max)

    return Signal(val)


def create(n, constructor, *args, **kwargs):
    """Helper function for constructing multiple objects with the same
    arguments.

    Shorthand for [constructor(\*args, \*\*kwargs) for i in range(n)]
    """
    return [constructor(*args, **kwargs) for i in range(n)]


def Sigs(n, *args, **kwargs):
    """Create multiple Signals cleanly.

    Args:
        n: number of signals to create.
        *args: passed through to :func:`.Sig`
        **kwargs: passed through to :func:`.Sig`

    Returns:
        [Sig(\*args, \*\*kwargs) for i in range(n)]
    """
    return create(n, Sig, *args, **kwargs)

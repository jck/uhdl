"""
uhdl.constructors
~~~~~~~~~~~~~

This module provides the core uhdl constructors.
"""

import random

from myhdl import intbv, EnumType, EnumItemType, Signal


#modbv is a subclass of intbv, so it can be skipped.
_myhdltypes = (intbv, EnumType, EnumItemType)


def bits(n=None, val=None, min=None, max=None):
    """Constructs a :class:`myhdl.intbv` object.

    Simplify the frequent cases of creating bit oriented objects(intbv/bool)

    Args:
        n (int): Bit width
        val (int): Inital value
        min (int): Minimum value; Used only if max is specified.
        max (int): Maximum value; Overrides bits argument.

    Returns:
        intbv or bool

    Examples:
        bits() == intbv()

        bits(0), bits(1) == False, True

        bits(n) == intbv()[n:]

        bits(n, v) == intbv(v)[n:]

        bits(min=i, max=j) == intbv(val=i, min=i, max=j)

        bits(val=x, min=i, max=j) == intbv(val=x, min=i, max=j)
    """

    if all(v is None for v in (n, min, max)):
        return intbv(val or 0)

    if min or max:
        if n:
            raise ValueError("bitwidth with min/max")
        if not max:
            raise ValueError("min without max")
        if not min:
            min = 0
        if val is None:
            val = min
        obj = intbv(val=val, min=min, max=max)
    elif type(n) == int:
        if n in (0, 1):
            obj = bool(n)
        else:
            if not val:
                val = 0
            obj = intbv(val)[n:]
    else:
        raise ValueError

    return obj


def randbits(n=0, min=None, max=None):
    """Create random bits easily, for simulations.

    Passes arguments to :func:`.bits` and changes the value to random.
    """
    bv = bits(n=n, min=min, max=max)
    if isinstance(bv, bool):
        return random.choice([True, False])

    if len(bv) == 0:
        raise ValueError("Unspecified bit width")
    bv[:] = random.getrandbits(len(bv))
    return bv


def Sig(*args, **kwargs):
    """Create Signals with the same API as :func:`.bits`.

    If the first argument is a bool or a myhdl type, a :class:`myhdl.Signal`
    is constructed of it.

    Else, arguments pass through to :func:`bits` and a :class:`myhdl.Signal`
    is constructed from the returned object.
    """
    if any((args, kwargs)):
        if args and isinstance(args[0], _myhdltypes + (bool,)):
            obj = args[0]
        else:
            obj = bits(*args, **kwargs)
    else:
        obj = None

    return Signal(obj)


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

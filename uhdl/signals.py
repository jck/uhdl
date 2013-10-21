import random

import myhdl
from myhdl import instance, always, delay, Signal, intbv, modbv

from .helpers import create


def bits(n=0, val=None, min=None, max=None):
    """
    Simplify the frequent cases of creating bit oriented objects

    Args:
        n (int): Bit width
        val (int): Inital value
        min (int): Minimum value; Used only if max is specified.
        max (int): Maximum value; Overrides bits argument.

    Returns:
        intbv or bool
    """

    if min or max:
        if n:
            raise ValueError("bitwidth with min/max")
        if not max:
            raise ValueError("min without max")
        if not min:
            min = 0
        if not val:
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
    bv = bits(n=n, min=min, max=max)
    bv[:] = random.getrandbits(len(bv))
    return bv


def Sig(*args, **kwargs):
    """ if bits(args, kwargs) Signal"""
    if any((args, kwargs)):
        if args and isinstance(args[0], (bool, intbv, modbv)):
            obj = args[0]
        else:
            obj = bits(*args, **kwargs)
    else:
        obj = None

    return Signal(obj)


def Sigs(n, *args, **kwargs):
    """
    Create multiple Signals easily.
    """
    return create(n, Sig, *args, **kwargs)


class Clock(myhdl.SignalType):
    """Clock class for use in simulations"""
    def __init__(self, period=2):
        self.period = period
        if period % 2 != 0:
            raise ValueError("period must be divisible by 2")

        super(Clock, self).__init__(False)

    def gen(self):

        @always(delay(self.period/2))
        def _clock():
            self.next = not self
        return _clock


class Reset(myhdl.ResetSignal):
    """Reset class for use in simulations"""
    def __init__(self, val=0, active=0, async=True):
        super(Reset, self).__init__(val, active, async)

    def gen(self, time=5):

        @instance
        def _reset():
            self.next = self.active
            yield delay(time)
            self.next = not self.active

        return _reset


    #def pulse(self, delays=10):
        #if isinstance(delays, (int, long)):
            #self.next = self.active
            #yield delay(delays)
            #self.next = not self.active
        #elif isinstance(delays, tuple):
            #assert len(delays) in (1, 2, 3), "Incorrect number of delays"
            #self.next = not self.active if len(delays) == 3 else self.active
            #for dd in delays:
                #yield delay(dd)
                #self.next = not self.val
        #else:
            #raise ValueError("%s type not supported" % (type(d)))

"""
uhdl.sim
~~~~~~~~~~~~~~~~
This module provides objects which simplify simulations.

"""
from myhdl import SignalType, ResetSignal, delay, always, instance, Simulation

from decorator import decorator


class Clock(SignalType):
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


class Reset(ResetSignal):
    """Reset class for use in simulations"""
    def __init__(self, val=0, active=0, async=True):
        super(Reset, self).__init__(val, active, async)

    def pulse(self, time=5):

        @instance
        def _reset():
            self.next = self.active
            yield delay(time)
            self.next = not self.active

        return _reset


def run(*args, **params):
    """Magical function for running a :class:`myhdl.Simulation`

    Usable as a function or a decorator with optional parameters.

    Usage:

        As a function

        .. code-block:: python

            run(generators, duration=None, quiet=False)

        As a decorator

        .. code-block:: python

            @run
            def function_which_returns_generators(...):
                ...

            @run(duration=n, quiet=False)
            def function_which_returns_generators(...):
                ...
    """
    if not args:

        def _run(*args):
            return run(*args, **params)

        return _run
    elif len(args) == 1 and callable(args[0]):

        @decorator
        def deco(func, *args, **kwargs):
            return run(func(*args, **kwargs), **params)

        return deco(args[0])
    else:
        #print args, params
        return Simulation(*args).run(**params)

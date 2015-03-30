import functools

import wrapt
from myhdl import SignalType, ResetSignal, delay, always, instance, Simulation


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

def run_sim(*args, **kwargs):
    return Simulation(*args).run(**kwargs)


def sim(wrapped=None, duration=None, quiet=False):
    """Decorator which simplifies running a :class:`myhdl.Simulation`

    Usage:

        .. code-block:: python

            @sim
            def function_which_returns_generators(...):
                ...

            @sim(duration=n, quiet=False)
            def function_which_returns_generators(...):
                ...
    """
    if wrapped is None:
        return functools.partial(sim, duration=duration, quiet=quiet)

    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        return run_sim(wrapped(*args, **kwargs), duration=duration, quiet=quiet)

    return wrapper(wrapped)

"""
uhdl.sim
~~~~~~~~~~~~~~~~
This module provides objects which simplify simulations.

"""

from myhdl import SignalType, ResetSignal, delay, always, instance


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

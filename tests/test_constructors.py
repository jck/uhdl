from hypothesis import assume, given
from hypothesis.specifiers import integers_in_range
from myhdl import Signal, intbv

from uhdl import Sig

width = integers_in_range(2, 100)


def check_sigs(expected, *sigs):
    __tracebackhide__ = True
    for s in sigs:
        assert expected == s
        assert len(expected) == len(s)


@given(bool)
def test_bool(x):
    check_sigs(Signal(x), Sig(x))


@given(width)
def test_only_width(x):
    check_sigs(Signal(intbv()[x:]), Sig(w=x))


@given(int, width)
def test_width_and_initial_value(val, width):
    check_sigs(Signal(intbv(val)[width:]),
               Sig(val, width),
               Sig(val, w=width),
               Sig(val=val, w=width)
               )


@given(int, int)
def test_min_max(min, max):
    assume(min < max)
    check_sigs(Signal(intbv(val=min, min=min, max=max)), Sig(min=min, max=max))

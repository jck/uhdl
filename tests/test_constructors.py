from hypothesis import assume, given
from hypothesis.specifiers import integers_in_range
from myhdl import Signal, intbv

from uhdl import Sig

width = integers_in_range(2, 100)

def test_noargs():
    assert Sig() == Signal()


@given(bool)
def test_bool(x):
    assert Sig(x) == Signal(x)


@given(width)
def test_only_width(x):
    expected = Signal(intbv())
    assert Sig(x) == expected
    assert Sig(n=x) == expected


@given(width, int)
def test_width_and_initial_value(width, initial):
    expected = Signal(intbv(initial)[width:])
    assert Sig(width, initial) == expected
    assert Sig(width, val=initial) == expected
    assert Sig(n=width, val=initial) == expected


@given(int)
def test_only_max(x):
    assume(x > 0)
    assert Sig(max=x) == Signal(intbv(min=0, max=x))


@given(int, int)
def test_min_max(min, max):
    assume(min < max)
    assert Sig(min=min, max=max) == Signal(intbv(val=min, min=min, max=max))

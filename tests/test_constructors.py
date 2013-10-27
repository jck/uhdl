from myhdl import Signal, intbv
from uhdl import Sig


def test_noargs():
    assert Sig() == Signal()


def test_bool():
    assert Sig(True) == Signal(True)
    assert Sig(False) == Signal(False)


def test_only_width():
    expected = Signal(intbv()[10:])
    assert Sig(10) == expected
    assert Sig(n=10) == expected


def test_width_and_initial_value():
    expected = Signal(intbv(20)[10:])
    assert Sig(10, 20) == expected
    assert Sig(10, val=20) == expected
    assert Sig(n=10, val=20) == expected


def test_only_max():
    assert Sig(max=50) == Signal(intbv(min=0, max=50))


def test_min_max():
    assert Sig(min=30, max=60) == Signal(intbv(val=30, min=30, max=60))
    assert Sig(val=40, min=30, max=60) == Signal(intbv(val=40, min=30, max=60))

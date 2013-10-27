import pytest

import uhdl.sim
from uhdl import run


@pytest.fixture(autouse=True)
def monkey_sim(monkeypatch):
    #print 'monkey business'
    class SimulationMonkey(object):
        def __init__(self, *args):
            self.args = args

        def run(self, **kwargs):
            return self.args, kwargs

    monkeypatch.setattr(uhdl.sim, 'Simulation', SimulationMonkey)


def test_onlyargs():
    assert run(1, 2, 3) == ((1, 2, 3), {})


def test_argsandkwargs():
    args = 1, 2, 3
    kwargs = dict(a=4, b=5)
    assert run(*args, **kwargs) == (args, kwargs)


def test_decorator_without_param():
    g = 1, 2, 3

    @run
    def test():
        return g

    assert test() == ((g,), {})


def test_decorator_with_param():
    g = 1, 2, 3

    @run(a=4, b=5)
    def test():
        return g

    assert test() == ((g,), dict(a=4, b=5))

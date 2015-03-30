import pytest

from uhdl import sim


@pytest.fixture(autouse=True)
def monkey_sim(monkeypatch):
    class SimulationMonkey(object):
        def __init__(self, *args):
            self.args = args

        def run(self, **kwargs):
            return self.args, kwargs

    monkeypatch.setattr('uhdl.helpers.Simulation', SimulationMonkey)


def test_decorator_without_param():
    g = 1, 2, 3

    @sim
    def test():
        return g

    assert test() == ((g,), dict(duration=None, quiet=False))


def test_decorator_with_param():
    g = 1, 2, 3

    @sim(duration=5)
    def test():
        return g

    assert test() == ((g,), dict(duration=5, quiet=False))

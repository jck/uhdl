import subprocess

from myhdl import always_comb, instance, StopSimulation, Simulation, delay
from uhdl import HW, Sigs, randbits, utils


def setup_module():
    utils.VPI.make('icarus')


def connect(ip, op):

    @always_comb
    def logic():
        op.next = ip

    return logic


a, b = Sigs(2, w=32)
dut = HW(connect, a, b)


def test_icarus_backend_simple(in_tmpdir):

    @instance
    def stim():
        for i in range(5):
            rand = randbits(32)
            a.next = rand
            yield delay(10)
            assert b == a

        raise StopSimulation

    gens = dut.sim(backend='icarus'), stim

    Simulation(gens).run()

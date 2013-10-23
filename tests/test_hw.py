from myhdl import always_comb, instance, StopSimulation, Simulation, delay
from uhdl import HW, Sigs, randbits


def connect(ip, op):

    @always_comb
    def logic():
        op.next = ip

    return logic


a, b = Sigs(2, 32)
dut = HW(connect, a, b)


def test_icarus_backend_simple():

    @instance
    def stim():
        for i in range(5):
            rand = randbits(32)
            a.next = rand
            yield delay(10)
            assert b == a

        raise StopSimulation

    Simulation(dut.sim(backend='icarus'), stim).run()
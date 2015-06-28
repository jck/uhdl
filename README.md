UHDL: Python Hardware Description for Humans.
=============================================

[![Travis](https://img.shields.io/travis/jck/uhdl/master.svg)][Travis]
[![Docs](https://readthedocs.org/projects/uhdl/badge/?version=latest)][Docs]
[![PyPI](https://img.shields.io/pypi/v/uhdl.svg)][PyPI]



UHDL is a BSD Licensed library which simplifies the process of designing
digital hardware with [MyHDL].

UHDL provides utilities to simplify constructing myhdl objects, A uniform
simulation API, and more.

To compile the cosimulation vpis, simply:

```bash
    $ uhdl vpi init
```

Usage Example:

```python
    from myhdl import always_seq, instance, StopSimulation
    from uhdl import Clock, Reset, Sig, randbits, HW, run

    def inc(clk, rst, en, count):
        @always_seq(clk.posedge, rst)
        def logic():
            if en:
                count.next = count + 1
        return logic

    #Simulation(test_inc()).run()
    @run
    def test_inc(backend):
        clk = Clock()
        rst = Reset(async=False)
        en = Sig(False)
        count = Sig(8) #Signal(intbv()[8:])
        top = HW(inc, clk, rst, en, count)
        dut = top.sim(backend=backend)

        @instance
        def stim():
            for i in range(20):
                en.next = randbits(1)
            raise StopSimulation

        @instance
        def mon():
            while True:
                yield clk.posedge
                yield delay(1)
                print rst, en, count

        #If the function was not decorated with @run, 
        #run(clk.gen(), rst.pulse(), dut, stim, mon) would do the trick.
        return clk.gen(), rst.pulse(5), dut, stim, mon

    #run with myhdl
    test_inc()
    #run with icarus
    test_inc('icarus')
    #run with modelsim
    test_inc('modelsim')
```

Features
--------
- Helper functions to simplify the common cases of Signal creation.
- Consistent simulation and conversion API with sane default arguments.
- Automatic HDL Simulator detection and VPI Compilation(icarus/modelsim).


Installation
------------
To install UHDL, simply:

```bash
    $ mkvirtualenv uhdl
    $ pip install uhdl
```

Documentation
-------------
Documentation is avaliable at http://uhdl.readthedocs.org/en/latest/api.html

[Docs]: https://uhdl.readthedocs.org
[PyPI]: https://pypi.python.org/pypi/uhdl
[Travis]: https://travis-ci.org/jck/uhdl
[MyHDL]: http://myhdl.org/

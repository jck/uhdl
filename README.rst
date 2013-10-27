=============================================
UHDL: Python Hardware Description for Humans.
=============================================

.. image:: https://badge.fury.io/py/uhdl.png
    :target: http://badge.fury.io/py/uhdl
    
.. image:: https://travis-ci.org/jck/uhdl.png?branch=master
        :target: https://travis-ci.org/jck/uhdl

.. image:: https://pypip.in/d/uhdl/badge.png
        :target: https://crate.io/packages/uhdl?version=latest


UHDL is a BSD Licensed library which simplifies the process of designing
digital hardware with MyHDL_.

UHDL provides utilities to simplify constructing myhdl objects, A uniform
simulation API, and more.


.. code-block:: python

    from myhdl import always_seq, instance, StopSimulation
    from uhdl import Clock, Reset, Sig, randbits, HW, run

    def inc(clk, rst, en, count):
        @always_seq(clk.posedge, rst)
        def logic():
            if en:
                count.next = count + 1
        return logic

    @run
    def test_inc(backend):
        clk = Clock()
        rst = Reset(async=False)
        en = Sig(False)
        count = Sig(8)
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

        return clk.gen(), rst.pulse(5), dut, stim, mon

    #run with myhdl
    test_inc()
    #run with icarus
    test_inc('icarus')
    #run with modelsim
    test_inc('modelsim')

Features
--------
- Helper functions to simplify the common cases of Signal creation.
- Consistent simulation and conversion API with sane default arguments.
- Automatic HDL Simulator detection and VPI Compilation(icarus/modelsim).
- Django style models for facilitating reuse of hardware structures [#sf]_.


Installation
------------
To install UHDL, simply:

.. code-block:: bash

    $ mkvirtualenv uhdl
    $ pip install uhdl

Documentation
-------------
Documentation is avaliable at http://uhdl.readthedocs.org/en/latest/api.html

.. rubric:: Footnotes.
.. [#sf] See sfaoenids_ for an example of using uhdl models for automatically 
    generating the HW-SW interface.

.. _MyHDL: http://myhdl.org/
.. _sfaoenids: https://github.com/jck/sfaoenids

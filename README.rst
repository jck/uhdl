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

    from uhdl import HW

    dut = HW(top, clk, rst, a, b)
    gens = [clk.gen(), rst.pulse(10), testbench()]
    # Simulate design with icarus verilog
    dut_gen = dut.sim(backend='icarus')
    # Maybe you don't want to see the wave forms..
    dut_gen = dut.sim(backend='icarus', trace=False)
    # Or, Simulate it with modelsim
    dut_gen = dut.sim(backend='modelsim', hdl='verilog')
    # Or, Just simulate it in myhdl
    dut_gen = dut.sim()
    #Convert and save it to a path?
    dut.convert(hdl='verilog', tb=False, path='path/to/somewhere')


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
Documentation is avaliable at http://uhdl.readthedocs.org/latest/api.html

.. rubric:: Footnotes.
.. [#sf] See sfaoenids_ for an example of using uhdl models for automatically 
    generating the HW-SW interface.

.. _MyHDL: http://myhdl.org/
.. _sfaoenids: https://github.com/jck/sfaoenids

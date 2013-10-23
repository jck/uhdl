"""
uhdl.backends.cosim
~~~~~~~~~~~~~~~~~~~
"""

import subprocess
import os

from clint import resources
from myhdl import Cosimulation

from uhdl.utils import classproperty, flatten


class cosim(object):
    """Decorator"""
    def __init__(self, func):
        self.func = func
        self.cmd = func.func_name

    def _reg(self, cls):
        delattr(cls, self.cmd)
        if cls.vpi:
            self.vpi = cls.vpi
        setattr(cls, 'cosim', self)

    def __call__(self, *args, **ports):
        cli_args = self.func(self.vpi, *args)
        cmd = ' '.join(flatten(self.cmd, cli_args))
        return Cosimulation(exe=cmd,  **ports)


class compile(object):
    """Decorator"""
    def __init__(self, hdl):
        self.hdl = hdl

    def __call__(self, func):
        self.func = func
        self.cmd = func.func_name
        return self

    def _reg(self, cls):
        delattr(cls, self.cmd)
        cls.compilers[self.hdl] = self.run

    def run(self, *args, **kwargs):
        cli_args = self.func(*args, **kwargs)
        cmd = flatten(self.cmd, cli_args)
        subprocess.check_call(cmd)


class CoSimulatorBase(type):
    """Metaclass for CoSimulator Base class"""
    def __init__(cls, name, bases, attrs):
        if not hasattr(cls, 'registry'):
            cls.registry = {}
        else:
            cls.registry[name] = cls
            cls.compilers = {}

            if not hasattr(cls, 'vpi_file'):
                cls.vpi_file = cls.vpi_path + '/{0}.vpi'.format(cls.__name__)

            for attr, obj in attrs.items():
                if isinstance(obj, (cosim, compile)):
                    obj._reg(cls)


class CoSimulator(object):
    """Base class for all CoSimulators"""
    __metaclass__ = CoSimulatorBase
    resources.init('uhdl', 'uhdl')
    vpi_path = resources.user.sub('vpi').path

    @classproperty
    def vpi(cls):
        if os.path.exists(cls.vpi_file):
            return cls.vpi_file
        else:
            return None

    @classmethod
    def compile(cls, hdl, *args, **kwargs):
        return cls.compilers[hdl](*args, **kwargs)


class icarus(CoSimulator):

    @compile('verilog')
    def iverilog(ip, op):
        cli_args = '-o', op, ip
        return cli_args

    @cosim
    def vvp(vpi, o):
        cli_args = '-m', vpi, o
        return cli_args


class modelsim(CoSimulator):

    @compile('vhdl')
    def vcom(ip, op):
        raise NotImplementedError

    @compile('verilog')
    def vlog(ip, op):
        raise NotImplementedError

    @cosim
    def vsim(vpi, o):
        raise NotImplementedError

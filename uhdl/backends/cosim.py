"""
uhdl.backends.cosim
~~~~~~~~~~~~~~~~~~~
"""

import subprocess
import os

from clint import resources
from myhdl import Cosimulation

from uhdl.utils import classproperty, flatten, which


resources.init('uhdl', 'uhdl')
vpi_path = resources.user.sub('vpi').path


class cosim(object):
    """Decorator for specifying how to run the simulation executable.

    For use inside CoSimulator classes. See icarus and modelsim for usage
    examples.
    """
    def __init__(self, func):
        self.func = func
        self.cmd = func.func_name

    def _reg(self, cls):
        self.cls = cls
        setattr(cls, 'cosim', self)

    def __call__(self, *args, **ports):
        cli_args = self.func(self.cls.vpi, *args)
        cmd = ' '.join(flatten(self.cmd, cli_args))
        return Cosimulation(exe=cmd,  **ports)


class compile(object):
    """Decorator for specifying how to compile hdl.

    For use inside CoSimulator classes. See icarus and modelsim for usage
    examples.
    """
    def __init__(self, hdl):
        self.hdl = hdl

    def __call__(self, func):
        self.func = func
        self.cmd = func.func_name
        return self

    def _reg(self, cls):
        cls.compilers[self.hdl] = self.run

    def run(self, *args, **kwargs):
        cli_args = self.func(*args, **kwargs)
        cmd = flatten(self.cmd, cli_args)
        subprocess.check_call(cmd)


class CoSimulatorBase(type):
    """Metaclass for CoSimulator Base class"""
    def __init__(cls, name, bases, attrs):
        if not hasattr(cls, 'registry'):
            #Base class
            cls.registry = {}
        else:
            #Subclasses
            cls.registry[name] = cls
            cls.compilers = {}

            #set default vpi file path to resources dir
            if not hasattr(cls, 'vpi'):
                cls.vpi = vpi_path + '/{0}.vpi'.format(cls.__name__)

            for attr, obj in attrs.items():
                if isinstance(obj, (cosim, compile)):
                    delattr(cls, attr)
                    obj._reg(cls)


class CoSimulator(object):
    """Base class for all CoSimulators"""
    __metaclass__ = CoSimulatorBase

    @classproperty
    def exists(cls):
        """Check if the cosimulator's executable exists in the PATH"""
        return which(cls.cosim.cmd) is not None

    @classproperty
    def vpi_exists(cls):
        """Check if the vpi for the cosimulator exists."""
        return os.path.exists(cls.vpi)

    @classmethod
    def compile(cls, hdl, *args, **kwargs):
        return cls.compilers[hdl](*args, **kwargs)

    @classmethod
    def cosim_gen(cls, hdl, files, portmap):
        op = files[0].split('.')[0]
        cls.compile(hdl, files, op)
        return cls.cosim(op, **portmap)


class icarus(CoSimulator):

    @compile('verilog')
    def iverilog(ip, op):
        cli_args = '-o', op+'.o', ip
        return cli_args

    @cosim
    def vvp(vpi, op):
        cli_args = '-m', vpi, op+'.o'
        return cli_args


class modelsim(CoSimulator):

    @compile('vhdl')
    def vcom(ip, op):
        raise NotImplementedError

    @compile('verilog')
    def vlog(ip, op):
        subprocess.call(['vlib', 'work_'+op])
        cli_args = '-work', 'work_'+op, ip
        return cli_args

    @cosim
    def vsim(vpi, op):
        top = 'work_{0}.tb_{0}'.format(op)
        do = '-do', vpi_path + '/cosim.do'
        cli_args = '-c', '-quiet', '-pli', vpi, top, do
        return cli_args

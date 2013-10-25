"""
uhdl.

Usage:
    uhdl vpi init [-f] [-t] [<simulator>...]

Arguments:
    <simulator>     Supported simulators: {sims}. [default: all].

Options:
    -h --help       Show this screen.True
    --version       Show version.
    -f --force      Recompile VPIs even if they already exist.
    -t --test       Run MyHDL Cosimulation tests after compilation.
"""

from __future__ import print_function
import imp
import sys
import subprocess
import shutil
import os

from clint import resources
from clint.textui import colored
from docopt import docopt

from . import __version__
from .backends import CoSimulator
from .utils import cd


def error(msg):
    sys.stdout.flush()
    print ('{0} {1}'.format(colored.red('ERROR:'), msg))
    sys.exit(1)


def main():
    doc = __doc__.format(sims=', '.join(CoSimulator.registry.keys()))
    args = docopt(doc, version=__version__)
    if args['vpi']:
        sims = args['<simulator>']
        force = args['--force']
        test = args['--test']
        vpi_init(sims, force=force, test=test)


def myhdl_dir():
    return imp.find_module('myhdl')[1]


def vpi_init(sims, force=False, test=False):
    supported = CoSimulator.registry
    support_str = ', '.join(supported.keys())
    if sims:
        if not set(sims).issubset(supported):
            error('Currently supported simulators: {0}'.format(support_str))
        sims = [supported[s] for s in sims]
        for s in sims:
            if not s.exists:
                error('Simulator {0} not found'.format(s.__name__))
    else:
        sims = find_cosimulators()
        if not sims:
            print('No simulators found, exiting.')
            sys.exit()
        sims_str = ', '.join(s.__name__ for s in sims)
        print('Found simulators: {0}.'.format(sims_str))

    resources.init('uhdl', 'uhdl')
    vpi_path = resources.user.sub('vpi')
    cosim_dir = os.path.abspath(myhdl_dir() + '/../cosimulation')
    with cd(cosim_dir):
        for s in sims:
            name = s.__name__
            if s.vpi_exists and not force:
                print('VPI for {0} already exists.'.format(name))
                continue
            with cd(name):
                make_vpi(name, dest=vpi_path)
                if test:
                    test_vpi(name)


def find_cosimulators():
    return [s for s in CoSimulator.registry.values() if s.exists]


def make_vpi(name, dest):
    print('\nCompiling {0} vpi:'.format(name))
    env = {}
    vpi_name = 'myhdl.vpi'
    if name == 'modelsim':
        vpi_name = 'myhdl_vpi.so'
        vsim = subprocess.check_output('which vsim', shell=True)
        env['INCS'] = '-I ' + os.path.abspath(vsim+'/../../include')
        dest.write('cosim.do', 'run -all; quit')

    if env:
        os.environ.update(env)
        subprocess.check_call(['make', '-e'])
    else:
        subprocess.check_call(['make'])

    shutil.copy(vpi_name, dest.path)


def test_vpi(name):
    print('\nTesting {0} vpi:'.format(name))
    with cd('./test'):
        if name == 'modelsim':
            shutil.copy('../myhdl_vpi.so', '.')
            if not os.path.exists('./work'):
                subprocess.check_call(['vlib', 'work'])

        subprocess.check_call(['python', 'test_all.py'])

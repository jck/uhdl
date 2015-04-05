import sys
import subprocess
import shutil
import os

from clint import resources
import click

from .backends import CoSimulator
from .utils import cd


@click.group()
def cli():
    pass


@cli.group()
def vpi():
    """Manage cosimulation VPI modules"""
    pass


def cosim_srcdir():
    cache = resources.cache.path
    cosim_dir = os.path.abspath(cache + '/cosimulation')

    if not os.path.exists(cosim_dir):
        shutil.copytree(os.path.join(sys.prefix, 'share/myhdl/cosimulation'),
                        cosim_dir)

    return cosim_dir

supported_sims = CoSimulator.registry.keys()
installed_sims = [s.__name__ for s in CoSimulator.registry.values() if s.exists]

class SimParamType(click.ParamType):
    name = 'simulator'

    def convert(self, value, param, ctx):
        if value not in CoSimulator.registry.keys():
            self.fail('%s is not a supported simulator' % value, param, ctx)
        if value not in installed_sims:
            self.fail('%s is not installed' % value, param, ctx)
        return value

SIM = SimParamType()


@vpi.command('init')
@click.option('--force', is_flag=True,
              help='Recompile VPIs even if they already exist')
@click.argument('simulators', nargs=-1, type=SIM)
def vpi_init(simulators, force):
    """Compile Cosimulation VPI modules"""
    if not simulators:
        simulators = installed_sims

    if not simulators:
        click.secho('No simulators found, exiting.', fg='red')
        sys.exit()

    sims = [CoSimulator.registry[k] for k in simulators]

    with cd(cosim_srcdir()):
        for s in sims:
            name = s.__name__
            if s.vpi_exists and not force:
                click.echo('VPI for {0} already exists.'.format(name))
                continue
            with cd(name):
                make_vpi(name, dest=s.vpi)


def make_vpi(name, dest):
    click.echo('\nCompiling {0} vpi:'.format(name))
    vpi_name = {
        'icarus': 'myhdl.vpi',
        'modelsim': 'myhdl_vpi.so'
    }
    if name == 'modelsim':
        vpi_path = resources.user.sub('vpi')
        vpi_path.write('cosim.do', 'run -all; quit')

    subprocess.check_call(['make'])

    click.echo('\nTesting {0} vpi:'.format(name))
    with cd('./test'):
        if name == 'modelsim':
            shutil.copy('../myhdl_vpi.so', '.')
            if not os.path.exists('./work'):
                subprocess.check_call(['vlib', 'work'])

        subprocess.check_call(['python', 'test_all.py'])

    shutil.copy(vpi_name[name], dest)


@vpi.command('clean')
def vpi_clean():
    shutil.rmtree(resources.user.sub('vpi').path)
    shutil.rmtree(resources.cache.sub('myhdl').path)

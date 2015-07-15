import sys
import subprocess
import shutil
import os

from tempfile import mkdtemp

import click

from .backends import CoSimulator
from .utils import cd, VPI


@click.group(context_settings={
    'help_option_names': ['-h', '--help']
})
def cli():
    pass


@cli.group()
def vpi():
    """Manage cosimulation VPI modules"""
    pass


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

    for s in sims:
        name = s.__name__
        if s.vpi_exists and not force:
            click.echo('VPI for {0} already exists.'.format(name))
            continue
        VPI.make(name)


@vpi.command('clean')
def vpi_clean():
    VPI.clean()

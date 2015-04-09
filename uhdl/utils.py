"""
uhdl.utils
~~~~~~~~~~

Utility functions(unrelated to hardware desription) used within uhdl.
"""

import collections
import contextlib
import distutils.spawn
import os
import subprocess
import shutil
import sys
from functools import wraps
from tempfile import mkdtemp


def get_data_dir():
    plat = sys.platform
    if plat.startswith('linux'):
        data_dir = os.getenv('XDG_DATA_HOME', '~/.local/share')
    elif plat == 'darwin':
        data_dir = '~/Library/Application Support/'
    return os.path.join(os.path.expanduser(data_dir), 'uhdl')


class _VPI(object):
    dir = os.path.join(get_data_dir(), 'vpi')
    cosim_src = os.path.join(sys.prefix, 'share/myhdl/cosimulation')

    def __init__(self):
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)

    def make(self, name, force=False):
        dest = os.path.join(self.dir, name+'.vpi')
        print(dest)
        if not force and os.path.exists(dest):
            return

        tmpdir = mkdtemp()
        srcdir = os.path.join(tmpdir, 'cosim')
        shutil.copytree(os.path.join(self.cosim_src), srcdir)

        vpi_name = {
            'icarus': 'myhdl.vpi',
            'modelsim': 'myhdl_vpi.so'
        }
        with cd(os.path.join(srcdir, name)):
            subprocess.check_call(['make', 'test'])
            shutil.copy(vpi_name[name], dest)

    def clean(self):
        if os.path.exists(self.dir):
            shutil.rmtree(self.dir)

VPI = _VPI()


@contextlib.contextmanager
def cd(path):
    """Context manager which changes the current working directory

    Args:
        path(str): path to change directory to.

    Usage:
        .. code-block:: python

            with cd('path/to/somewhere'):
                #do something..

    """
    curdir = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(curdir)


def which(exe):
    return distutils.spawn.find_executable(exe)


class classproperty(object):
    """Decorator which allows read only class properties"""

    def __init__(self,  fget):
        self.fget = fget

    def __get__(self,  owner_self,  owner_cls):
        return self.fget(owner_cls)


def flatten(*args):
    """Flattens arbitrarily nested iterators(Except strings)

    Args:
        *args: objects and iterables.

    Returns:
        list of all objects.
    """
    l = []
    for arg in args:
        if isinstance(arg, collections.Iterable) and not isinstance(arg, str):
            for item in arg:
                l.extend(flatten(item))
        else:
            l.append(arg)
    return l


def memoize(func):
    cache = {}

    @wraps(func)
    def memoized(*args):
        if args in cache:
            result = cache[args]
        else:
            result = func(*args)
            cache[args] = result
        return result
    return memoized

import os
import hashlib

from uhdl import cli
from uhdl.backends import icarus
from uhdl.utils import cd


myhdl_dir = cli.myhdl_dir()
print myhdl_dir
cosim_dir = os.path.abspath(myhdl_dir + '/../cosimulation')


def md5sum(filename):
    md5 = hashlib.md5()
    with open(filename, 'rb') as f:
        for chunk in iter(lambda: f.read(128*md5.block_size), b''):
            md5.update(chunk)
    return md5.hexdigest()


def test_icarus_vpi():
    cli.vpi_init(['icarus'], force=True, test=False)
    with cd(cosim_dir):
        with cd('./icarus'):
            assert md5sum(icarus.vpi) == md5sum('myhdl.vpi')

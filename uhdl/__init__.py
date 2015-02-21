"""
UHDL
~~~~
"""

from __future__ import absolute_import

__version__ = '0.0.9'

#The version udhl is currently based on.
__myhdl__ = 'https://bitbucket.org/jck2/myhdl/get/sf-hotfixes.tar.gz#egg=myhdl'

from . import math
from . import models
from .constructors import bits, randbits, create, Sig, Sigs
from .sim import Clock, Reset, run
from .hw import HW

from __future__ import absolute_import
import math as _m


def log2(n):
    return int(_m.log(n, 2))


def clog2(n):
    return int(_m.ceil(_m.log(n, 2)))


def roundup(x, y):
    """round up x to nearest multiple of y"""
    n = x - (x % -y)
    return n

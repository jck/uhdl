import sys

PY2 = sys.version_info[0] == 2

def with_metaclass(meta, *bases):
    class metaclass(meta):
        __call__ = type.__call__
        __init__ = type.__init__
        def __new__(cls, name, this_bases, d):
            if this_bases is None:
                return type.__new__(cls, name, (), d)
            return meta(name, bases, d)
    return metaclass('temporary_class', None, {})

if not PY2:
    integer_types = (int,)
else:
    integer_types = (int, long)

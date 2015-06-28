import copy
import functools

import myhdl as _myhdl


class factory(object):
    def __init__(self, func):
        self.func = func
        functools.update_wrapper(self, func)

    def __call__(self, cls):
        cls._defaultfactory = self
        inst = cls()
        return inst

    def __get__(self, inst, cls):

        def from_cls(*args, **kwargs):
            inst = cls(*args, **kwargs)
            return self.func(inst._fields)

        def from_inst(*args, **kwargs):
            if args or kwargs:
                fields = cls(*args, **kwargs)._fields
            else:
                fields = copy.deepcopy(inst._fields)
            return self.func(fields)

        if inst:
            return from_inst
        else:
            return from_cls


@factory
class to_sigcon(object):
    def __init__(self, fields):
        self._fields = []
        for field in fields:
            s = _myhdl.Signal(field.obj)
            setattr(self, field.name, s)
            self._fields.append(s)

    def __iter__(self):
        return iter(self._fields)


@factory
class to_sigstruct(_myhdl.SignalType):
    def __init__(self, fields, *args, **kwargs):
        vals = [field.obj for field in fields]
        _myhdl.SignalType.__init__(self, _myhdl.concat(*vals))

        r = 0
        for field in reversed(fields):
            l = r + len(field.obj)
            setattr(self, field.name, self(l, r))
            r = l

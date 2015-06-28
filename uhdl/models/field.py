from myhdl import intbv as _intbv
import uhdl


class Field(object):
    creation_counter = 0

    def __init__(self, obj=None):
        if not hasattr(self, 'obj'):
            self.obj = obj
        self.creation_counter = Field.creation_counter
        Field.creation_counter += 1

    def __lt__(self, other):
        if isinstance(other, Field):
            return self.creation_counter < other.creation_counter
        return NotImplemented

    def __repr__(self):
        name = getattr(self, 'name', '')
        return '<Field {0}: {1}>'.format(name, repr(self.obj))


class bits(Field):

    def __init__(self, *args, **kwargs):
        # self._obj = uhdl.bits(*args, **kwargs)
        self._obj = _intbv()[args[0]:]
        if isinstance(self._obj, bool):
            self._obj = _intbv(self.obj)[1:]
        super(bits, self).__init__()

    @property
    def obj(self):
        return self._obj

    @obj.setter
    def obj(self, value):
        self._obj[:] = value

    #def __len__(self):
        #if isinstance(self._obj, bool):
            #return 1
        #else:
            #return len(self._obj)

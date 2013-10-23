"""
uhdl.structures
~~~~~~~~~~~~~~~

Data structures(unrelated to hardware description) used internally by uhdl.

"""
import collections


def _dictrepr(instance, store):
    name = instance.__class__.__name__
    return '{name}({store})'.format(name=name, store=store)


class DictRef(object):
    def __init__(self, store):
        self.__dict__['store'] = store

    def __getattr__(self, key):
        return self.__dict__['store'][key]

    def __setattr__(self, key, value):
        self.__dict__['store'][key] = value

    def __repr__(self):
        return _dictrepr(self, self._store)


class CaselessDict(collections.MutableMapping):
    def __init__(self, data=None, **kwargs):
        self._store = dict()
        if data is None:
            data = {}
        self.update(data, **kwargs)
        #self.key = DictRef(self)

    def __setitem__(self, key, value):
        self._store[key.lower()] = value

    def __getitem__(self, key):
        return self._store[key.lower()]

    def __delitem__(self, key):
        del self._store[key.lower()]

    def __iter__(self):
        return iter(self._store)

    def __len__(self):
        return len(self._store)

    def __repr__(self):
        return _dictrepr(self, self._store)

    #@property
    #def key(self):
        #return self._ref

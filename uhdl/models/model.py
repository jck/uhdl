import copy

from .field import Field
from .factory import to_sigcon, to_sigstruct

all_factories = (to_sigcon, to_sigstruct)


class Options(object):
    def __init__(self):
        self.fields = None
        self.factory = None
        self.factories = {}


class ModelBase(type):

    def __new__(cls, name, bases, attrs):
        super_new = super(ModelBase, cls).__new__

        #Ensure that initialization is performed only for subclasses of Model
        #(excluding Model class itself)
        parents = [b for b in bases if isinstance(b, ModelBase)]
        if not parents:
            return super_new(cls, name, bases, attrs)

        new_attrs = {'__module__': attrs.pop('__module__')}
        options = new_attrs['_meta'] = Options()
        new_class = super_new(cls, name, bases, new_attrs)

        fields = []
        for attr, obj in attrs.items():
            if isinstance(obj, Field):
                obj.name = attr
                fields.append(obj)
            else:
                new_attrs[attr] = obj

        options.fields = sorted(fields)
        #Setup the factory methods
        for factory in all_factories:
            setattr(new_class, factory.__name__, factory)

        return new_class


class Model(object):
    __metaclass__ = ModelBase

    def __init__(self, *args, **kwargs):
        self._fields = copy.deepcopy(self._meta.fields)
        fields_iter = iter(self._fields)
        for val, field in zip(args, fields_iter):
            field.obj = val
            setattr(self, field.name, field.obj)
            kwargs.pop(field.name, None)

        for field in fields_iter:
            if field.name in kwargs:
                field.obj = kwargs.pop(field.name)
            setattr(self, field.name, field.obj)

    def __call__(self, *args, **kwargs):
        if hasattr(self, '_defaultfactory'):
            return self._defaultfactory(*args, **kwargs)
        else:
            return self.__class__(*args, **kwargs)

    def __len__(self):
        return sum(len(f.obj) for f in self._fields)

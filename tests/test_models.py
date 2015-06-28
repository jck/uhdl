import uhdl.models as m


class simple(m.Model):
    a = m.bits(8)
    b = m.bits(8)


def test_classtype():
    assert type(simple) == m.model.ModelBase


def test_insttype():
    assert isinstance(simple(), m.model.Model)


def test_field_modification():
    inst = simple()
    print(inst())

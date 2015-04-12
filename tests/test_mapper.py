import pytest

from kim.exception import MapperError
from kim.mapper import Mapper
from kim.fields import Field


class TestType(object):
    pass


class TestField(Field):
    pass


def test_mapper_sets_declared_fields():
    """Ensure that on attributes inheriting from :class:`kim.fields.Field`
    are set in a mappers fields.
    """

    class MyTestMapper(Mapper):

        __type__ = TestType

        name = TestField()
        other = 'not a field'

    mapper_with_fields = MyTestMapper()
    assert 'name' in mapper_with_fields.declared_fields
    assert isinstance(mapper_with_fields.declared_fields['name'], TestField)
    assert 'other' not in mapper_with_fields.declared_fields


def test_mapper_must_define_mapper_type():
    """Ensure that a :class:`.MapperError` is raised if a :class:`.Mapper`
    fails to set its __type__ attr.
    """

    mapper = Mapper()
    with pytest.raises(MapperError):
        mapper.get_mapper_type()


def test_mapper_inheritance():
    """test inheriting from other mapper classes
    """

    class OtherField(Field):
        pass

    class MapperBase(Mapper):

        __type__ = TestType

        id = TestField()
        name = TestField()

    class NewMapper(MapperBase):

        __type__ = TestType

        id = OtherField()
        additional_field = TestField()

    mapper = MapperBase()
    other_mapper = NewMapper()

    assert len(mapper.declared_fields.keys()) == 2
    assert 'id' in mapper.declared_fields
    assert 'name' in mapper.declared_fields

    assert len(other_mapper.declared_fields.keys()) == 3
    assert 'id' in other_mapper.declared_fields
    assert 'name' in other_mapper.declared_fields
    assert 'additional_field' in other_mapper.declared_fields

    assert isinstance(other_mapper.declared_fields['id'], OtherField)


def test_get_mapper_type():

    class MapperBase(Mapper):

        __type__ = TestType

        id = TestField()

    mapper = MapperBase()
    assert mapper.get_mapper_type() == TestType


def test_order_of_fields():

    class MapperBase(Mapper):

        __type__ = TestType

        id = TestField()
        name = TestField()

    class MyMapper(MapperBase):

        email = TestField()

    class ThirdMapper(MyMapper):

        id = TestField()
        id._creation_order = 999

    mapper = MyMapper()
    assert ['id', 'name', 'email'] == list(mapper.declared_fields.keys())

    mapper = ThirdMapper()
    assert ['name', 'email', 'id'] == list(mapper.declared_fields.keys())

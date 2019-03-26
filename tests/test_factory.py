import pytest  # type: ignore
from typing import get_type_hints
import dataclasses

from dataclass_builder.factory import _create_fn
from dataclass_builder import (MissingFieldError, UndefinedFieldError,
                               REQUIRED, OPTIONAL, dataclass_builder, build)
from tests.conftest import (Circle, PixelCoord, Point,  # type: ignore
                            NoFields, NoInitFields, NotADataclass,
                            Build, Fields)
# from tests.conftest import (PixelCoord, Point, Circle, NotADataclass,
#                             NoFields, NoInitFields, ExtendedBuilder)


def test_create_fn():
    fn = _create_fn(
        'add', ['a: float', 'b: int'], ['return a + b'], {}, return_type=float)
    assert get_type_hints(fn)['a'] == float
    assert get_type_hints(fn)['b'] == int
    assert get_type_hints(fn)['return'] == float
    assert fn(5, 8) == 13

    # no return type
    fn = _create_fn(
        'add', ['a: float', 'b: int'], ['return a + b'], {})
    assert get_type_hints(fn)['a'] == float
    assert get_type_hints(fn)['b'] == int
    assert 'return' not in get_type_hints(fn)
    assert fn(5, 8) == 13

    # no argument type hints
    fn = _create_fn(
        'add', ['a', 'b'], ['return a + b'], {}, return_type=float)
    assert 'a' not in get_type_hints(fn)
    assert 'b' not in get_type_hints(fn)
    assert get_type_hints(fn)['return'] == float
    assert fn(5, 8) == 13

    # no type hints
    fn = _create_fn(
        'add', ['a', 'b'], ['return a + b'], {})
    assert get_type_hints(fn) == {}
    assert fn(5, 8) == 13

    # with environment
    fn = _create_fn(
        'add', ['a', 'b'], ['return a + b + c'], {'c': 100})
    assert fn(5, 8) == 113

    # without environment
    fn = _create_fn(
        'add', ['a', 'b'], ['return a + b'])
    assert fn(5, 8) == 13


def test_all_fields_set():
    # fields passed in constructor
    PixelCoordBuilder = dataclass_builder(PixelCoord)
    builder = PixelCoordBuilder(x=3, y=7)
    assert PixelCoord(3, 7) == build(builder)
    assert PixelCoord(3, 7) == builder.build()
    # fields set by assignment
    builder = PixelCoordBuilder()
    builder.x = 9
    builder.y = 1
    assert PixelCoord(9, 1) == build(builder)
    assert PixelCoord(9, 1) == builder.build()


def test_order_invariant():
    # fields passed in constructor
    PixelCoordBuilder = dataclass_builder(PixelCoord)
    builder = PixelCoordBuilder(y=7, x=3)
    assert PixelCoord(3, 7) == build(builder)
    assert PixelCoord(3, 7) == builder.build()
    # fields set by assignment
    builder = PixelCoordBuilder()
    builder.y = 1
    builder.x = 9
    assert PixelCoord(9, 1) == build(builder)
    assert PixelCoord(9, 1) == builder.build()


def test_repr():
    PixelCoordBuilder = dataclass_builder(PixelCoord)
    assert ('PixelCoordBuilder(x=3, y=7)' ==
            repr(PixelCoordBuilder(x=3, y=7)))
    assert ('PixelCoordBuilder(x=3, y=7)' ==
            repr(PixelCoordBuilder(y=7, x=3)))
    assert ('PixelCoordBuilder(x=3)' ==
            repr(PixelCoordBuilder(x=3)))
    assert ('PixelCoordBuilder(y=7)' ==
            repr(PixelCoordBuilder(y=7)))


def test_custom_name():
    PixelBuilder = dataclass_builder(PixelCoord, name='PixelBuilder')
    assert ('PixelBuilder(x=3, y=7)' ==
            repr(PixelBuilder(x=3, y=7)))
    assert ('PixelBuilder(x=3, y=7)' ==
            repr(PixelBuilder(y=7, x=3)))
    assert ('PixelBuilder(x=3)' ==
            repr(PixelBuilder(x=3)))
    assert ('PixelBuilder(y=7)' ==
            repr(PixelBuilder(y=7)))


def test_must_be_dataclass():
    with pytest.raises(TypeError):
        dataclass_builder(NotADataclass)


def test_missing_field():
    PixelCoordBuilder = dataclass_builder(PixelCoord)
    # fields passed in constructor
    builder = PixelCoordBuilder(y=7)
    with pytest.raises(MissingFieldError):
        build(builder)
    with pytest.raises(MissingFieldError):
        builder.build()
    try:
        build(builder)
    except MissingFieldError as err:
        assert err.dataclass == PixelCoord
        assert err.field == dataclasses.fields(PixelCoord)[0]
    try:
        builder.build()
    except MissingFieldError as err:
        assert err.dataclass == PixelCoord
        assert err.field == dataclasses.fields(PixelCoord)[0]
    # fields set by assignment
    builder = PixelCoordBuilder()
    builder.x = 9
    with pytest.raises(MissingFieldError):
        build(builder)
    with pytest.raises(MissingFieldError):
        builder.build()
    try:
        build(builder)
    except MissingFieldError as err:
        assert err.dataclass == PixelCoord
        assert err.field == dataclasses.fields(PixelCoord)[1]
    try:
        builder.build()
    except MissingFieldError as err:
        assert err.dataclass == PixelCoord
        assert err.field == dataclasses.fields(PixelCoord)[1]


def test_undefined_field():
    PixelCoordBuilder = dataclass_builder(PixelCoord)
    # fields passed in constructor
    # TODO: Make this raise an UndefinedFieldError
    with pytest.raises(TypeError):
        PixelCoordBuilder(z=10)
    # fields set by assignment
    builder = PixelCoordBuilder()
    with pytest.raises(UndefinedFieldError):
        builder.z = 1
    try:
        builder.z = 1
    except UndefinedFieldError as err:
        assert err.dataclass == PixelCoord
        assert err.field == 'z'


def test_optional_field_not_required():
    PointBuilder = dataclass_builder(Point)
    # fields passed in constructor
    builder = PointBuilder(x=3.0, y=7.0)
    assert Point(3.0, 7.0, 1.0) == build(builder)
    assert Point(3.0, 7.0, 1.0) == builder.build()
    # fields set by assignment
    builder = PointBuilder(Point)
    builder.x = 9.0
    builder.y = 1.0
    assert Point(9.0, 1.0, 1.0) == build(builder)
    assert Point(9.0, 1.0, 1.0) == builder.build()


def test_optional_field_can_be_set():
    PointBuilder = dataclass_builder(Point)
    # fields passed in constructor
    builder = PointBuilder(x=3.0, y=7.0, w=0.3)
    assert Point(3.0, 7.0, 0.3) == build(builder)
    assert Point(3.0, 7.0, 0.3) == builder.build()
    # fields set by assignment
    builder = PointBuilder()
    builder.x = 9.0
    builder.y = 1.0
    builder.w = 1.7
    assert Point(9.0, 1.0, 1.7) == build(builder)
    assert Point(9.0, 1.0, 1.7) == builder.build()


def test_init_false_field_not_required():
    CircleBuilder = dataclass_builder(Circle)
    # fields passed in constructor
    builder = CircleBuilder(radius=3.0)
    assert Circle(3.0) == build(builder)
    assert Circle(3.0) == builder.build()
    # fields set by assignment
    builder = CircleBuilder()
    builder.radius = 9.0
    assert Circle(9.0) == build(builder)
    assert Circle(9.0) == builder.build()


def test_init_false_field_cannot_be_set():
    CircleBuilder = dataclass_builder(Circle)
    # fields passed in constructor
    # TODO: Make this raise an UndefinedFieldError
    with pytest.raises(TypeError):
        CircleBuilder(radius=3.0, area=10)
    # fields set by assignment
    builder = CircleBuilder()
    with pytest.raises(UndefinedFieldError):
        builder.area = 1
    try:
        builder.area = 1
    except UndefinedFieldError as err:
        assert err.dataclass == Circle
        assert err.field == 'area'


def test_handles_dataclass_without_fields():
    NoFieldsBuilder = dataclass_builder(NoFields)
    builder = NoFieldsBuilder()
    assert NoFields() == build(builder)
    assert NoFields() == builder.build()
    NoInitFieldsBuilder = dataclass_builder(NoInitFields)
    builder = NoInitFieldsBuilder()
    assert NoInitFields() == build(builder)
    assert NoInitFields() == builder.build()


def test_access_unset_field():
    # TODO: Change how the wrapper works so it behaves like this.
    PointBuilder = dataclass_builder(Point)
    builder = PointBuilder()
    assert builder.x == REQUIRED
    assert builder.y == REQUIRED
    assert builder.w == OPTIONAL


def test_access_invalid_field():
    PointBuilder = dataclass_builder(Point)
    builder = PointBuilder()
    with pytest.raises(AttributeError):
        print(builder.i)


class ExtendedBuilder(dataclass_builder(Point)):
    pass


def test_class_inheritance():
    builder = ExtendedBuilder(y=4, w=10)
    builder.x = 8
    assert Point(8, 4, 10) == build(builder)
    assert Point(8, 4, 10) == builder.build()


def test_build_field():
    BuildBuilder = dataclass_builder(Build)
    builder = BuildBuilder(build='taken')
    assert builder.build == 'taken'
    assert Build('taken') == build(builder)


def test_fields_field():
    FieldsBuilder = dataclass_builder(Fields)
    builder = FieldsBuilder(fields='taken')
    assert builder.fields == 'taken'

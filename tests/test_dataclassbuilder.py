import pytest  # type: ignore

import dataclasses
from dataclass_builder import (DataclassBuilder, MissingFieldError,
                               UndefinedFieldError, build)
from tests.conftest import (PixelCoord, Point, Circle,  # type: ignore
                            NotADataclass, NoFields, NoInitFields,
                            ExtendedBuilder)


def test_all_fields_set():
    # fields passed in constructor
    builder = DataclassBuilder(PixelCoord, x=3, y=7)
    assert PixelCoord(3, 7) == build(builder)
    # fields set by assignment
    builder = DataclassBuilder(PixelCoord)
    builder.x = 9
    builder.y = 1
    assert PixelCoord(9, 1) == build(builder)


def test_order_invariant():
    # fields passed in constructor
    builder = DataclassBuilder(PixelCoord, y=7, x=3)
    assert PixelCoord(3, 7) == build(builder)
    # fields set by assignment
    builder = DataclassBuilder(PixelCoord)
    builder.y = 1
    builder.x = 9
    assert PixelCoord(9, 1) == build(builder)


def test_repr():
    assert ('DataclassBuilder(PixelCoord, x=3, y=7)' ==
            repr(DataclassBuilder(PixelCoord, x=3, y=7)))
    assert ('DataclassBuilder(PixelCoord, x=3, y=7)' ==
            repr(DataclassBuilder(PixelCoord, y=7, x=3)))
    assert ('DataclassBuilder(PixelCoord, x=3)' ==
            repr(DataclassBuilder(PixelCoord, x=3)))
    assert ('DataclassBuilder(PixelCoord, y=7)' ==
            repr(DataclassBuilder(PixelCoord, y=7)))


def test_must_be_dataclass():
    with pytest.raises(TypeError):
        DataclassBuilder(NotADataclass)


def test_missing_field():
    # fields passed in constructor
    builder = DataclassBuilder(PixelCoord, y=7)
    with pytest.raises(MissingFieldError):
        build(builder)
    try:
        build(builder)
    except MissingFieldError as err:
        assert err.dataclass == PixelCoord
        assert err.field == dataclasses.fields(PixelCoord)[0]
    # fields set by assignment
    builder = DataclassBuilder(PixelCoord)
    builder.x = 9
    with pytest.raises(MissingFieldError):
        build(builder)
    try:
        build(builder)
    except MissingFieldError as err:
        assert err.dataclass == PixelCoord
        assert err.field == dataclasses.fields(PixelCoord)[1]


def test_undefined_field():
    # fields passed in constructor
    with pytest.raises(UndefinedFieldError):
        DataclassBuilder(PixelCoord, z=10)
    try:
        DataclassBuilder(PixelCoord, z=10)
    except UndefinedFieldError as err:
        assert err.dataclass == PixelCoord
        assert err.field == 'z'
    # fields set by assignment
    builder = DataclassBuilder(PixelCoord)
    with pytest.raises(UndefinedFieldError):
        builder.z = 1
    try:
        builder.z = 1
    except UndefinedFieldError as err:
        assert err.dataclass == PixelCoord
        assert err.field == 'z'


def test_optional_field_not_required():
    # fields passed in constructor
    builder = DataclassBuilder(Point, x=3.0, y=7.0)
    assert Point(3.0, 7.0, 1.0) == build(builder)
    # fields set by assignment
    builder = DataclassBuilder(Point)
    builder.x = 9.0
    builder.y = 1.0
    assert Point(9.0, 1.0, 1.0) == build(builder)


def test_optional_field_can_be_set():
    # fields passed in constructor
    builder = DataclassBuilder(Point, x=3.0, y=7.0, w=0.3)
    assert Point(3.0, 7.0, 0.3) == build(builder)
    # fields set by assignment
    builder = DataclassBuilder(Point)
    builder.x = 9.0
    builder.y = 1.0
    builder.w = 1.7
    assert Point(9.0, 1.0, 1.7) == build(builder)


def test_init_false_field_not_required():
    # fields passed in constructor
    builder = DataclassBuilder(Circle, radius=3.0)
    assert Circle(3.0) == build(builder)
    # fields set by assignment
    builder = DataclassBuilder(Circle)
    builder.radius = 9.0
    assert Circle(9.0) == build(builder)


def test_init_false_field_cannot_be_set():
    # fields passed in constructor
    with pytest.raises(UndefinedFieldError):
        DataclassBuilder(Circle, radius=3.0, area=10)
    try:
        DataclassBuilder(Circle, radius=3.0, area=10)
    except UndefinedFieldError as err:
        assert err.dataclass == Circle
        assert err.field == 'area'
    # fields set by assignment
    builder = DataclassBuilder(Circle)
    with pytest.raises(UndefinedFieldError):
        builder.area = 1
    try:
        builder.area = 1
    except UndefinedFieldError as err:
        assert err.dataclass == Circle
        assert err.field == 'area'


def test_handles_dataclass_without_fields():
    builder = DataclassBuilder(NoFields)
    assert NoFields() == build(builder)
    builder = DataclassBuilder(NoInitFields)
    assert NoInitFields() == build(builder)


def test_access_unset_field():
    builder = DataclassBuilder(Point)
    with pytest.raises(AttributeError):
        print(builder.x)


def test_access_invalid_field():
    builder = DataclassBuilder(Point)
    with pytest.raises(AttributeError):
        print(builder.i)


def test_class_inheritance():
    builder = ExtendedBuilder(Point, y=4, w=10)
    builder.x = 8
    assert Point(8, 4, 10) == build(builder)

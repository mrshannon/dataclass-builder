import dataclasses

import pytest  # type: ignore

from dataclass_builder import (
    OPTIONAL,
    REQUIRED,
    DataclassBuilder,
    MissingFieldError,
    UndefinedFieldError,
    build,
    fields,
)
from tests.conftest import (
    Circle,
    ExtendedBuilder,
    NoFields,
    NoInitFields,
    NotADataclass,
    PixelCoord,
    Point,
    Types,
    Typing,
)


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


def test_no_positional_arguments():
    with pytest.raises(TypeError):
        DataclassBuilder(PixelCoord, 3, 5)  # type: ignore
    with pytest.raises(TypeError):
        DataclassBuilder(NoFields, 3)  # type: ignore


def test_repr():
    assert "DataclassBuilder(PixelCoord, x=3, y=7)" == repr(
        DataclassBuilder(PixelCoord, x=3, y=7)
    )
    assert "DataclassBuilder(PixelCoord, x=3, y=7)" == repr(
        DataclassBuilder(PixelCoord, y=7, x=3)
    )
    assert "DataclassBuilder(PixelCoord, x=3)" == repr(
        DataclassBuilder(PixelCoord, x=3)
    )
    assert "DataclassBuilder(PixelCoord, y=7)" == repr(
        DataclassBuilder(PixelCoord, y=7)
    )


def test_repr_with_strings():
    assert "DataclassBuilder(Types, int_=1, float_=1.0, str_='one')" == repr(
        DataclassBuilder(Types, int_=1, float_=1.0, str_="one")
    )
    assert "DataclassBuilder(Types, float_=1.0, str_='one')" == repr(
        DataclassBuilder(Types, float_=1.0, str_="one")
    )
    assert "DataclassBuilder(Types, str_='one')" == repr(
        DataclassBuilder(Types, str_="one")
    )


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
    with pytest.raises(TypeError):
        DataclassBuilder(PixelCoord, z=10)
    # fields set by assignment
    builder = DataclassBuilder(PixelCoord)
    with pytest.raises(UndefinedFieldError):
        builder.z = 1
    try:
        builder.z = 1
    except UndefinedFieldError as err:
        assert err.dataclass == PixelCoord
        assert err.field == "z"


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
    with pytest.raises(TypeError):
        DataclassBuilder(Circle, radius=3.0, area=10)
    # fields set by assignment
    builder = DataclassBuilder(Circle)
    with pytest.raises(UndefinedFieldError):
        builder.area = 1
    try:
        builder.area = 1
    except UndefinedFieldError as err:
        assert err.dataclass == Circle
        assert err.field == "area"


def test_handles_dataclass_without_fields():
    builder = DataclassBuilder(NoFields)
    assert NoFields() == build(builder)
    builder = DataclassBuilder(NoInitFields)
    assert NoInitFields() == build(builder)


def test_access_unset_field():
    builder = DataclassBuilder(Point)
    assert builder.x == REQUIRED
    assert builder.y == REQUIRED
    assert builder.w == OPTIONAL


def test_access_invalid_field():
    builder = DataclassBuilder(Point)
    with pytest.raises(AttributeError):
        print(builder.i)


def test_fields_returns_settable_fields():
    fields_ = fields(DataclassBuilder(PixelCoord))
    assert ["x", "y"] == list(fields_.keys())
    assert ["x", "y"] == [f.name for f in fields_.values()]
    assert [int, int] == [f.type for f in fields_.values()]

    fields_ = fields(DataclassBuilder(Point))
    assert ["x", "y", "w"] == list(fields_.keys())
    assert ["x", "y", "w"] == [f.name for f in fields_.values()]
    assert [float, float, float] == [f.type for f in fields_.values()]

    fields_ = fields(DataclassBuilder(Circle))
    assert ["radius"] == list(fields_.keys())
    assert ["radius"] == [f.name for f in fields_.values()]
    assert [float] == [f.type for f in fields_.values()]

    fields_ = fields(DataclassBuilder(Types))
    assert ["int_", "float_", "str_"] == list(fields_.keys())
    assert ["int_", "float_", "str_"] == [f.name for f in fields_.values()]
    assert [int, float, str] == [f.type for f in fields_.values()]


def test_fields_returns_required_fields():
    fields_ = fields(DataclassBuilder(PixelCoord), optional=False)
    assert ["x", "y"] == list(fields_.keys())
    assert ["x", "y"] == [f.name for f in fields_.values()]
    assert [int, int] == [f.type for f in fields_.values()]

    fields_ = fields(DataclassBuilder(Point), optional=False)
    assert ["x", "y"] == list(fields_.keys())
    assert ["x", "y"] == [f.name for f in fields_.values()]
    assert [float, float] == [f.type for f in fields_.values()]

    fields_ = fields((DataclassBuilder(Circle)), optional=False)
    assert ["radius"] == list(fields_.keys())
    assert ["radius"] == [f.name for f in fields_.values()]
    assert [float] == [f.type for f in fields_.values()]

    fields_ = fields(DataclassBuilder(Types), optional=False)
    assert ["int_", "float_"] == list(fields_.keys())
    assert ["int_", "float_"] == [f.name for f in fields_.values()]
    assert [int, float] == [f.type for f in fields_.values()]


def test_fields_returns_optional_fields():
    fields_ = fields(DataclassBuilder(PixelCoord), required=False)
    assert [] == list(fields_.keys())
    assert [] == [f.name for f in fields_.values()]
    assert [] == [f.type for f in fields_.values()]

    fields_ = fields(DataclassBuilder(Point), required=False)
    assert ["w"] == list(fields_.keys())
    assert ["w"] == [f.name for f in fields_.values()]
    assert [float] == [f.type for f in fields_.values()]

    fields_ = fields(DataclassBuilder(Circle), required=False)
    assert [] == list(fields_.keys())
    assert [] == [f.name for f in fields_.values()]
    assert [] == [f.type for f in fields_.values()]

    fields_ = fields(DataclassBuilder(Types), required=False)
    assert ["str_"] == list(fields_.keys())
    assert ["str_"] == [f.name for f in fields_.values()]
    assert [str] == [f.type for f in fields_.values()]


def test_fields_returns_no_fields():
    fields_ = fields(DataclassBuilder(PixelCoord), required=False, optional=False)
    assert [] == list(fields_.keys())
    assert [] == [f.name for f in fields_.values()]
    assert [] == [f.type for f in fields_.values()]

    fields_ = fields(DataclassBuilder(Point), required=False, optional=False)
    assert [] == list(fields_.keys())
    assert [] == [f.name for f in fields_.values()]
    assert [] == [f.type for f in fields_.values()]

    fields_ = fields(DataclassBuilder(Circle), required=False, optional=False)
    assert [] == list(fields_.keys())
    assert [] == [f.name for f in fields_.values()]
    assert [] == [f.type for f in fields_.values()]

    fields_ = fields(DataclassBuilder(Types), required=False, optional=False)
    assert [] == list(fields_.keys())
    assert [] == [f.name for f in fields_.values()]
    assert [] == [f.type for f in fields_.values()]


def test_class_inheritance():
    builder = ExtendedBuilder(Point, y=4, w=10)
    builder.x = 8
    assert Point(8, 4, 10) == build(builder)
    fields_ = fields(ExtendedBuilder(Types))
    assert ["int_", "float_", "str_"] == list(fields_.keys())
    assert ["int_", "float_", "str_"] == [f.name for f in fields_.values()]
    assert [int, float, str] == [f.type for f in fields_.values()]


def test_typing_module():
    builder = DataclassBuilder(Typing)
    builder.sequence = [1, 2, 3]
    builder.mapping = {"one": 1.0, "two": 2.0, "pi": 3.14}

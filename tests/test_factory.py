import dataclasses
from typing import Any, get_type_hints

import pytest  # type: ignore

from dataclass_builder import (
    OPTIONAL,
    REQUIRED,
    MissingFieldError,
    UndefinedFieldError,
    build,
    dataclass_builder,
    fields,
)
from dataclass_builder.factory import _create_fn
from tests.conftest import (
    Build,
    Circle,
    Fields,
    NoFields,
    NoInitFields,
    NotADataclass,
    PixelCoord,
    Point,
    Types,
    Typing,
)


def test_create_fn():
    fn = _create_fn(
        "add", ["a: float", "b: int"], ["return a + b"], {}, return_type=float
    )
    assert get_type_hints(fn)["a"] == float
    assert get_type_hints(fn)["b"] == int
    assert get_type_hints(fn)["return"] == float
    assert fn(5, 8) == 13

    # no return type
    fn = _create_fn("add", ["a: float", "b: int"], ["return a + b"], {})
    assert get_type_hints(fn)["a"] == float
    assert get_type_hints(fn)["b"] == int
    assert "return" not in get_type_hints(fn)
    assert fn(5, 8) == 13

    # no argument type hints
    fn = _create_fn("add", ["a", "b"], ["return a + b"], {}, return_type=float)
    assert "a" not in get_type_hints(fn)
    assert "b" not in get_type_hints(fn)
    assert get_type_hints(fn)["return"] == float
    assert fn(5, 8) == 13

    # no type hints
    fn = _create_fn("add", ["a", "b"], ["return a + b"], {})
    assert get_type_hints(fn) == {}
    assert fn(5, 8) == 13

    # with environment
    fn = _create_fn("add", ["a", "b"], ["return a + b + c"], {"c": 100})
    assert fn(5, 8) == 113

    # without environment
    fn = _create_fn("add", ["a", "b"], ["return a + b"])
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


def test_no_positional_arguments():
    PixelCoordBuilder = dataclass_builder(PixelCoord)
    with pytest.raises(TypeError):
        PixelCoordBuilder(3, 5)
    NoFieldsBuilder = dataclass_builder(NoFields)
    with pytest.raises(TypeError):
        NoFieldsBuilder(3)


def test_repr():
    PixelCoordBuilder = dataclass_builder(PixelCoord)
    assert "PixelCoordBuilder(x=3, y=7)" == repr(PixelCoordBuilder(x=3, y=7))
    assert "PixelCoordBuilder(x=3, y=7)" == repr(PixelCoordBuilder(y=7, x=3))
    assert "PixelCoordBuilder(x=3)" == repr(PixelCoordBuilder(x=3))
    assert "PixelCoordBuilder(y=7)" == repr(PixelCoordBuilder(y=7))


def test_repr_with_strings():
    TypesBuilder = dataclass_builder(Types)
    assert "TypesBuilder(int_=1, float_=1.0, str_='one')" == repr(
        TypesBuilder(int_=1, float_=1.0, str_="one")
    )
    assert "TypesBuilder(float_=1.0, str_='one')" == repr(
        TypesBuilder(float_=1.0, str_="one")
    )
    assert "TypesBuilder(str_='one')" == repr(TypesBuilder(str_="one"))


def test_custom_name():
    PixelBuilder = dataclass_builder(PixelCoord, name="PixelBuilder")
    assert "PixelBuilder(x=3, y=7)" == repr(PixelBuilder(x=3, y=7))
    assert "PixelBuilder(x=3, y=7)" == repr(PixelBuilder(y=7, x=3))
    assert "PixelBuilder(x=3)" == repr(PixelBuilder(x=3))
    assert "PixelBuilder(y=7)" == repr(PixelBuilder(y=7))


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
        assert err.field == "z"


def test_optional_field_not_required():
    PointBuilder = dataclass_builder(Point)
    # fields passed in constructor
    builder = PointBuilder(x=3.0, y=7.0)
    assert Point(3.0, 7.0, 1.0) == build(builder)
    assert Point(3.0, 7.0, 1.0) == builder.build()
    # fields set by assignment
    builder = PointBuilder()
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
        assert err.field == "area"


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


def test_build_field():
    BuildBuilder = dataclass_builder(Build)
    builder = BuildBuilder(build="taken")
    assert builder.build == "taken"
    assert Build("taken") == build(builder)


def test_fields_field():
    FieldsBuilder = dataclass_builder(Fields)
    builder = FieldsBuilder(fields="taken")
    assert builder.fields == "taken"
    fields_ = fields(builder)
    assert ["fields"] == list(fields_.keys())
    assert ["fields"] == [f.name for f in fields_.values()]
    assert [str] == [f.type for f in fields_.values()]


def test_fields_returns_settable_fields():
    PixelCoordBuilder = dataclass_builder(PixelCoord)
    fields_ = fields(PixelCoordBuilder())
    assert fields_ == PixelCoordBuilder().fields()
    assert ["x", "y"] == list(fields_.keys())
    assert ["x", "y"] == [f.name for f in fields_.values()]
    assert [int, int] == [f.type for f in fields_.values()]

    PointBuilder = dataclass_builder(Point)
    fields_ = fields(PointBuilder())
    assert fields_ == PointBuilder().fields()
    assert ["x", "y", "w"] == list(fields_.keys())
    assert ["x", "y", "w"] == [f.name for f in fields_.values()]
    assert [float, float, float] == [f.type for f in fields_.values()]

    CircleBuilder = dataclass_builder(Circle)
    fields_ = fields(CircleBuilder())
    assert fields_ == CircleBuilder().fields()
    assert ["radius"] == list(fields_.keys())
    assert ["radius"] == [f.name for f in fields_.values()]
    assert [float] == [f.type for f in fields_.values()]

    TypesBuilder = dataclass_builder(Types)
    fields_ = fields(TypesBuilder())
    assert fields_ == TypesBuilder().fields()
    assert ["int_", "float_", "str_"] == list(fields_.keys())
    assert ["int_", "float_", "str_"] == [f.name for f in fields_.values()]
    assert [int, float, str] == [f.type for f in fields_.values()]


def test_fields_returns_required_fields():
    PixelCoordBuilder = dataclass_builder(PixelCoord)
    fields_ = fields(PixelCoordBuilder(), optional=False)
    assert fields_ == PixelCoordBuilder().fields(optional=False)
    assert ["x", "y"] == list(fields_.keys())
    assert ["x", "y"] == [f.name for f in fields_.values()]
    assert [int, int] == [f.type for f in fields_.values()]

    PointBuilder = dataclass_builder(Point)
    fields_ = fields(PointBuilder(), optional=False)
    assert fields_ == PointBuilder().fields(optional=False)
    assert ["x", "y"] == list(fields_.keys())
    assert ["x", "y"] == [f.name for f in fields_.values()]
    assert [float, float] == [f.type for f in fields_.values()]

    CircleBuilder = dataclass_builder(Circle)
    fields_ = fields(CircleBuilder(), optional=False)
    assert fields_ == CircleBuilder().fields(optional=False)
    assert ["radius"] == list(fields_.keys())
    assert ["radius"] == [f.name for f in fields_.values()]
    assert [float] == [f.type for f in fields_.values()]

    TypesBuilder = dataclass_builder(Types)
    fields_ = fields(TypesBuilder(), optional=False)
    assert fields_ == TypesBuilder().fields(optional=False)
    assert ["int_", "float_"] == list(fields_.keys())
    assert ["int_", "float_"] == [f.name for f in fields_.values()]
    assert [int, float] == [f.type for f in fields_.values()]


def test_fields_returns_optional_fields():
    PixelCoordBuilder = dataclass_builder(PixelCoord)
    fields_ = fields(PixelCoordBuilder(), required=False)
    assert fields_ == PixelCoordBuilder().fields(required=False)
    assert [] == list(fields_.keys())
    assert [] == [f.name for f in fields_.values()]
    assert [] == [f.type for f in fields_.values()]

    PointBuilder = dataclass_builder(Point)
    fields_ = fields(PointBuilder(), required=False)
    assert fields_ == PointBuilder().fields(required=False)
    assert ["w"] == list(fields_.keys())
    assert ["w"] == [f.name for f in fields_.values()]
    assert [float] == [f.type for f in fields_.values()]

    CircleBuilder = dataclass_builder(Circle)
    fields_ = fields(CircleBuilder(), required=False)
    assert fields_ == CircleBuilder().fields(required=False)
    assert [] == list(fields_.keys())
    assert [] == [f.name for f in fields_.values()]
    assert [] == [f.type for f in fields_.values()]

    TypesBuilder = dataclass_builder(Types)
    fields_ = fields(TypesBuilder(), required=False)
    assert fields_ == TypesBuilder().fields(required=False)
    assert ["str_"] == list(fields_.keys())
    assert ["str_"] == [f.name for f in fields_.values()]
    assert [str] == [f.type for f in fields_.values()]


def test_fields_returns_no_fields():
    PixelCoordBuilder = dataclass_builder(PixelCoord)
    fields_ = fields(PixelCoordBuilder(), required=False, optional=False)
    assert fields_ == PixelCoordBuilder().fields(required=False, optional=False)
    assert [] == list(fields_.keys())
    assert [] == [f.name for f in fields_.values()]
    assert [] == [f.type for f in fields_.values()]

    PointBuilder = dataclass_builder(Point)
    fields_ = fields(PointBuilder(), required=False, optional=False)
    assert fields_ == PointBuilder().fields(required=False, optional=False)
    assert [] == list(fields_.keys())
    assert [] == [f.name for f in fields_.values()]
    assert [] == [f.type for f in fields_.values()]

    CircleBuilder = dataclass_builder(Circle)
    fields_ = fields(CircleBuilder(), required=False, optional=False)
    assert fields_ == CircleBuilder().fields(required=False, optional=False)
    assert [] == list(fields_.keys())
    assert [] == [f.name for f in fields_.values()]
    assert [] == [f.type for f in fields_.values()]

    TypesBuilder = dataclass_builder(Types)
    fields_ = fields(TypesBuilder(), required=False, optional=False)
    assert fields_ == TypesBuilder().fields(required=False, optional=False)
    assert [] == list(fields_.keys())
    assert [] == [f.name for f in fields_.values()]
    assert [] == [f.type for f in fields_.values()]


_PointBuilder: Any = dataclass_builder(Point, name="_PointBuilder")
_TypesBuilder: Any = dataclass_builder(Types, name="_TypesBuilder")


class ExtendedPointBuilder(_PointBuilder):
    pass


class ExtendedTypesBuilder(_TypesBuilder):
    pass


def test_class_inheritance():
    builder = ExtendedPointBuilder(y=4, w=10)
    builder.x = 8
    assert Point(8, 4, 10) == build(builder)
    assert Point(8, 4, 10) == builder.build()
    fields_ = fields(ExtendedTypesBuilder())
    assert ["int_", "float_", "str_"] == list(fields_.keys())
    assert ["int_", "float_", "str_"] == [f.name for f in fields_.values()]
    assert [int, float, str] == [f.type for f in fields_.values()]


def test_init_annotations():
    TypesBuilder = dataclass_builder(Types)
    builder = TypesBuilder()
    annotations = get_type_hints(builder.__init__)
    assert annotations == {
        "int_": int,
        "float_": float,
        "str_": str,
        "return": type(None),
    }


def test_build_annotations():
    TypesBuilder = dataclass_builder(Types)
    builder = TypesBuilder()
    annotations = get_type_hints(builder.build)
    assert annotations["return"] == Types
    annotations = get_type_hints(builder._build)
    assert annotations["return"] == Types


def test_typing_module():
    TypingBuilder = dataclass_builder(Typing)
    builder = TypingBuilder()
    builder.sequence = [1, 2, 3]
    builder.mapping = {"one": 1.0, "two": 2.0, "pi": 3.14}

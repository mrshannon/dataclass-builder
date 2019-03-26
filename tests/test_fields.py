from dataclass_builder import DataclassBuilder, fields
from tests.conftest import (PixelCoord, Point, Circle, Types,  # type: ignore
                            ExtendedBuilder)


def test_returns_settable_fields():
    fields_ = fields(DataclassBuilder(PixelCoord))
    assert ['x', 'y'] == list(fields_.keys())
    assert ['x', 'y'] == [f.name for f in fields_.values()]
    assert [int, int] == [f.type for f in fields_.values()]

    fields_ = fields(DataclassBuilder(Point))
    assert ['x', 'y', 'w'] == list(fields_.keys())
    assert ['x', 'y', 'w'] == [f.name for f in fields_.values()]
    assert [float, float, float] == [f.type for f in fields_.values()]

    fields_ = fields(DataclassBuilder(Circle))
    assert ['radius'] == list(fields_.keys())
    assert ['radius'] == [f.name for f in fields_.values()]
    assert [float] == [f.type for f in fields_.values()]

    fields_ = fields(DataclassBuilder(Types))
    assert ['int_', 'float_', 'str_'] == list(fields_.keys())
    assert ['int_', 'float_', 'str_'] == [f.name for f in fields_.values()]
    assert [int, float, str] == [f.type for f in fields_.values()]


def test_returns_required_fields():
    fields_ = fields(DataclassBuilder(PixelCoord), optional=False)
    assert ['x', 'y'] == list(fields_.keys())
    assert ['x', 'y'] == [f.name for f in fields_.values()]
    assert [int, int] == [f.type for f in fields_.values()]

    fields_ = fields(DataclassBuilder(Point), optional=False)
    assert ['x', 'y'] == list(fields_.keys())
    assert ['x', 'y'] == [f.name for f in fields_.values()]
    assert [float, float] == [f.type for f in fields_.values()]

    fields_ = fields((DataclassBuilder(Circle)), optional=False)
    assert ['radius'] == list(fields_.keys())
    assert ['radius'] == [f.name for f in fields_.values()]
    assert [float] == [f.type for f in fields_.values()]

    fields_ = fields(DataclassBuilder(Types), optional=False)
    assert ['int_', 'float_'] == list(fields_.keys())
    assert ['int_', 'float_'] == [f.name for f in fields_.values()]
    assert [int, float] == [f.type for f in fields_.values()]


def test_returns_optional_fields():
    fields_ = fields(DataclassBuilder(PixelCoord), required=False)
    assert [] == list(fields_.keys())
    assert [] == [f.name for f in fields_.values()]
    assert [] == [f.type for f in fields_.values()]

    fields_ = fields(DataclassBuilder(Point), required=False)
    assert ['w'] == list(fields_.keys())
    assert ['w'] == [f.name for f in fields_.values()]
    assert [float] == [f.type for f in fields_.values()]

    fields_ = fields(DataclassBuilder(Circle), required=False)
    assert [] == list(fields_.keys())
    assert [] == [f.name for f in fields_.values()]
    assert [] == [f.type for f in fields_.values()]

    fields_ = fields(DataclassBuilder(Types), required=False)
    assert ['str_'] == list(fields_.keys())
    assert ['str_'] == [f.name for f in fields_.values()]
    assert [str] == [f.type for f in fields_.values()]


def test_returns_no_fields():
    fields_ = fields(DataclassBuilder(PixelCoord),
                     required=False, optional=False)
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
    fields_ = fields(ExtendedBuilder(Types))
    assert ['int_', 'float_', 'str_'] == list(fields_.keys())
    assert ['int_', 'float_', 'str_'] == [f.name for f in fields_.values()]
    assert [int, float, str] == [f.type for f in fields_.values()]

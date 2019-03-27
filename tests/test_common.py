from dataclasses import fields

from dataclass_builder._common import (
    REQUIRED, OPTIONAL, MISSING,
    _is_settable, _is_required, _is_optional,
    _settable_fields, _required_fields, _optional_fields)
from tests.conftest import PixelCoord, Point, Circle, Types  # type: ignore


def test_constants():
    assert REQUIRED == REQUIRED
    assert REQUIRED != OPTIONAL
    assert OPTIONAL == OPTIONAL
    assert OPTIONAL != REQUIRED
    assert repr(REQUIRED) == 'REQUIRED'
    assert repr(OPTIONAL) == 'OPTIONAL'


def test_required_and_optional_are_missing():
    assert REQUIRED == MISSING
    assert MISSING == REQUIRED
    assert OPTIONAL == MISSING
    assert MISSING == OPTIONAL
    assert MISSING != 1
    assert MISSING != 'other'
    assert repr(MISSING) == 'MISSING'


def test_is_settable():
    assert _is_settable(fields(Types)[0])
    assert _is_settable(fields(Types)[1])
    assert _is_settable(fields(Types)[2])
    assert not _is_settable(fields(Types)[3])


def test_is_required():
    assert _is_required(fields(Types)[0])
    assert _is_required(fields(Types)[1])
    assert not _is_required(fields(Types)[2])
    assert not _is_required(fields(Types)[3])


def test_is_optional():
    assert not _is_optional(fields(Types)[0])
    assert not _is_optional(fields(Types)[1])
    assert _is_optional(fields(Types)[2])
    assert not _is_optional(fields(Types)[3])


def test_settable_fields():
    fields_ = _settable_fields(PixelCoord)
    assert ['x', 'y'] == list(fields_.keys())
    assert ['x', 'y'] == [f.name for f in fields_.values()]
    assert [int, int] == [f.type for f in fields_.values()]

    fields_ = _settable_fields(Point)
    assert ['x', 'y', 'w'] == list(fields_.keys())
    assert ['x', 'y', 'w'] == [f.name for f in fields_.values()]
    assert [float, float, float] == [f.type for f in fields_.values()]

    fields_ = _settable_fields(Circle)
    assert ['radius'] == list(fields_.keys())
    assert ['radius'] == [f.name for f in fields_.values()]
    assert [float] == [f.type for f in fields_.values()]

    fields_ = _settable_fields(Types)
    assert ['int_', 'float_', 'str_'] == list(fields_.keys())
    assert ['int_', 'float_', 'str_'] == [f.name for f in fields_.values()]
    assert [int, float, str] == [f.type for f in fields_.values()]


def test_required_fields():
    fields_ = _required_fields(PixelCoord)
    assert ['x', 'y'] == list(fields_.keys())
    assert ['x', 'y'] == [f.name for f in fields_.values()]
    assert [int, int] == [f.type for f in fields_.values()]

    fields_ = _required_fields(Point)
    assert ['x', 'y'] == list(fields_.keys())
    assert ['x', 'y'] == [f.name for f in fields_.values()]
    assert [float, float] == [f.type for f in fields_.values()]

    fields_ = _required_fields(Circle)
    assert ['radius'] == list(fields_.keys())
    assert ['radius'] == [f.name for f in fields_.values()]
    assert [float] == [f.type for f in fields_.values()]

    fields_ = _required_fields(Types)
    assert ['int_', 'float_'] == list(fields_.keys())
    assert ['int_', 'float_'] == [f.name for f in fields_.values()]
    assert [int, float] == [f.type for f in fields_.values()]


def test_optional_fields():
    fields_ = _optional_fields(PixelCoord)
    assert [] == list(fields_.keys())
    assert [] == [f.name for f in fields_.values()]
    assert [] == [f.type for f in fields_.values()]

    fields_ = _optional_fields(Point)
    assert ['w'] == list(fields_.keys())
    assert ['w'] == [f.name for f in fields_.values()]
    assert [float] == [f.type for f in fields_.values()]

    fields_ = _optional_fields(Circle)
    assert [] == list(fields_.keys())
    assert [] == [f.name for f in fields_.values()]
    assert [] == [f.type for f in fields_.values()]

    fields_ = _optional_fields(Types)
    assert ['str_'] == list(fields_.keys())
    assert ['str_'] == [f.name for f in fields_.values()]
    assert [str] == [f.type for f in fields_.values()]

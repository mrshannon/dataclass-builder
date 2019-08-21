from copy import copy, deepcopy
from dataclasses import fields

from dataclass_builder._common import (
    MISSING,
    OPTIONAL,
    REQUIRED,
    _is_optional,
    _is_required,
    _is_settable,
    _optional_fields,
    _required_fields,
    _settable_fields,
)
from tests.conftest import Circle, PixelCoord, Point, Types


def test_constants():
    assert REQUIRED is REQUIRED
    assert REQUIRED is not OPTIONAL
    assert REQUIRED is not MISSING
    assert OPTIONAL is OPTIONAL
    assert OPTIONAL is not REQUIRED
    assert OPTIONAL is not MISSING
    assert MISSING is MISSING
    assert MISSING is not REQUIRED
    assert MISSING is not OPTIONAL


def test_constants_repr():
    assert repr(REQUIRED) == "REQUIRED"
    assert repr(OPTIONAL) == "OPTIONAL"
    assert repr(MISSING) == "MISSING"


def test_constants_after_copy():
    assert copy(REQUIRED) is REQUIRED
    assert copy(REQUIRED) is not OPTIONAL
    assert copy(REQUIRED) is not MISSING
    assert copy(OPTIONAL) is OPTIONAL
    assert copy(OPTIONAL) is not REQUIRED
    assert copy(OPTIONAL) is not MISSING
    assert copy(MISSING) is MISSING
    assert copy(MISSING) is not REQUIRED
    assert copy(MISSING) is not OPTIONAL


def test_constants_after_deepcopy():
    assert deepcopy(REQUIRED) is REQUIRED
    assert deepcopy(REQUIRED) is not OPTIONAL
    assert deepcopy(REQUIRED) is not MISSING
    assert deepcopy(OPTIONAL) is OPTIONAL
    assert deepcopy(OPTIONAL) is not REQUIRED
    assert deepcopy(OPTIONAL) is not MISSING
    assert deepcopy(MISSING) is MISSING
    assert deepcopy(MISSING) is not REQUIRED
    assert deepcopy(MISSING) is not OPTIONAL


def test_required_and_optional_are_missing():
    assert REQUIRED == MISSING
    assert MISSING == REQUIRED
    assert OPTIONAL == MISSING
    assert MISSING == OPTIONAL
    assert MISSING != 1
    assert MISSING != "other"


def test_required_and_optional_are_missing_after_copy():
    assert copy(REQUIRED) == MISSING
    assert copy(MISSING) == REQUIRED
    assert copy(OPTIONAL) == MISSING
    assert copy(MISSING) == OPTIONAL


def test_required_and_optional_are_missing_after_deepcopy():
    assert deepcopy(REQUIRED) == MISSING
    assert deepcopy(MISSING) == REQUIRED
    assert deepcopy(OPTIONAL) == MISSING
    assert deepcopy(MISSING) == OPTIONAL


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
    assert ["x", "y"] == list(fields_.keys())
    assert ["x", "y"] == [f.name for f in fields_.values()]
    assert [int, int] == [f.type for f in fields_.values()]

    fields_ = _settable_fields(Point)
    assert ["x", "y", "w"] == list(fields_.keys())
    assert ["x", "y", "w"] == [f.name for f in fields_.values()]
    assert [float, float, float] == [f.type for f in fields_.values()]

    fields_ = _settable_fields(Circle)
    assert ["radius"] == list(fields_.keys())
    assert ["radius"] == [f.name for f in fields_.values()]
    assert [float] == [f.type for f in fields_.values()]

    fields_ = _settable_fields(Types)
    assert ["int_", "float_", "str_"] == list(fields_.keys())
    assert ["int_", "float_", "str_"] == [f.name for f in fields_.values()]
    assert [int, float, str] == [f.type for f in fields_.values()]


def test_required_fields():
    fields_ = _required_fields(PixelCoord)
    assert ["x", "y"] == list(fields_.keys())
    assert ["x", "y"] == [f.name for f in fields_.values()]
    assert [int, int] == [f.type for f in fields_.values()]

    fields_ = _required_fields(Point)
    assert ["x", "y"] == list(fields_.keys())
    assert ["x", "y"] == [f.name for f in fields_.values()]
    assert [float, float] == [f.type for f in fields_.values()]

    fields_ = _required_fields(Circle)
    assert ["radius"] == list(fields_.keys())
    assert ["radius"] == [f.name for f in fields_.values()]
    assert [float] == [f.type for f in fields_.values()]

    fields_ = _required_fields(Types)
    assert ["int_", "float_"] == list(fields_.keys())
    assert ["int_", "float_"] == [f.name for f in fields_.values()]
    assert [int, float] == [f.type for f in fields_.values()]


def test_optional_fields():
    fields_ = _optional_fields(PixelCoord)
    assert [] == list(fields_.keys())
    assert [] == [f.name for f in fields_.values()]
    assert [] == [f.type for f in fields_.values()]

    fields_ = _optional_fields(Point)
    assert ["w"] == list(fields_.keys())
    assert ["w"] == [f.name for f in fields_.values()]
    assert [float] == [f.type for f in fields_.values()]

    fields_ = _optional_fields(Circle)
    assert [] == list(fields_.keys())
    assert [] == [f.name for f in fields_.values()]
    assert [] == [f.type for f in fields_.values()]

    fields_ = _optional_fields(Types)
    assert ["str_"] == list(fields_.keys())
    assert ["str_"] == [f.name for f in fields_.values()]
    assert [str] == [f.type for f in fields_.values()]

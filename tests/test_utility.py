from dataclass_builder.utility import update
from dataclass_builder.wrapper import DataclassBuilder
from tests.conftest import PixelCoord, Point


def test_update():
    pixel = PixelCoord(2, 3)
    builder = DataclassBuilder(PixelCoord)
    builder.y = 4
    update(pixel, builder)
    assert pixel == PixelCoord(2, 4)


def test_update_with_defaults():
    point = Point(1.5, 2.3, 3.3)
    builder = DataclassBuilder(Point)
    builder.y = 1.1
    update(point, builder)
    assert point == Point(1.5, 1.1, 3.3)
    builder.w = 5.0
    update(point, builder)
    assert point == Point(1.5, 1.1, 5.0)

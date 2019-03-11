import math
from dataclasses import dataclass, field


@dataclass
class PixelCoord:
    x: int
    y: int


@dataclass
class Point:
    x: float
    y: float
    w: float = 1.0


@dataclass
class Circle:
    radius: float
    area: float = field(init=False)

    def __post_init__(self):
        self.area = math.pi*self.radius**2


@dataclass
class Types:
    int_: int
    float_: float
    str_: str = 'hello'


class NotADataclass:
    i: int
    j: int

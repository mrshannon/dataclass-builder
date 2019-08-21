import math
from dataclasses import dataclass, field
from typing import Mapping, Sequence

from dataclass_builder import DataclassBuilder


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
        self.area = math.pi * self.radius ** 2


@dataclass
class Types:
    int_: int
    float_: float
    str_: str = "hello"
    message: str = field(default="hello", init=False)


class NotADataclass:
    i: int
    j: int


@dataclass
class NoFields:
    pass


@dataclass
class NoInitFields:
    message: str = field(default="hello", init=False)


class ExtendedBuilder(DataclassBuilder):
    pass


@dataclass
class Build:
    build: str


@dataclass
class Fields:
    fields: str


@dataclass
class Typing:
    sequence: Sequence[int]
    mapping: Mapping[str, float]

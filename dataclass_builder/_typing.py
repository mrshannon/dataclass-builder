"""Special types for this package."""

from typing_extensions import Protocol, runtime, TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Mapping
    from dataclasses import Field

__all__ = ['Dataclass']


@runtime
class DataclassType(Protocol):
    """Protocol to match dataclasses."""

    __dataclass_fields__: 'Mapping[str, Field[Any]]'
    __base__: type


@runtime
class Dataclass(Protocol):
    """Protocol to match dataclasses and dataclass instances."""

    __dataclass_fields__: 'Mapping[str, Field[Any]]'

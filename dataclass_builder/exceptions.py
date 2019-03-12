"""Exceptions for the package.

.. _dataclass: https://docs.python.org/3/library/dataclasses.html
"""

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from dataclasses import Field

__all__ = ['DataclassBuilderError', 'UndefinedFieldError', 'MissingFieldError']


class DataclassBuilderError(Exception):
    """Base class of errors raised by :class:`DataclassBuilder`."""


class UndefinedFieldError(DataclassBuilderError):
    """Exception thrown when attempting to assign to an invalid field.

    Parameters
    ----------
    message
        Human readable error message
    dataclass
        Dataclass the :class:`DataclassBuilder` was made for.
    field
        Name of the invalid field that the calling code tried to assign to.

    Attributes
    ----------
    dataclass
        Dataclass the :class:`DataclassBuilder` was made for.
    field
        Name of the invalid field that the calling code tried to assign to.
    """

    def __init__(self, message: str, dataclass: Any, field: str) -> None:
        super().__init__(message)
        self.dataclass = dataclass
        self.field = field


class MissingFieldError(DataclassBuilderError):
    """Thrown when fields are missing when building a dataclass_ object.

    Parameters
    ----------
    message
        Human readable error message
    dataclass
        Dataclass the :class:`DataclassBuilder` was made for.
    field
        The :class:`dataclasses.Field` representing the missing field that
        needs to be assigned.

    Attributes
    ----------
    dataclass
        Dataclass the :class:`DataclassBuilder` was made for.
    field
        The :class:`dataclasses.Field` representing the missing field that
        needs to be assigned.

    """

    def __init__(self, message: str, dataclass: Any, field: 'Field[Any]') \
            -> None:
        super().__init__(message)
        self.dataclass = dataclass
        self.field = field

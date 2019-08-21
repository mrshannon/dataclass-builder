"""Exceptions for the package."""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from dataclasses import Field

__all__ = ["DataclassBuilderError", "UndefinedFieldError", "MissingFieldError"]


class DataclassBuilderError(Exception):
    """Base class of errors raised by :class:`DataclassBuilder`."""


class UndefinedFieldError(DataclassBuilderError):
    """Exception thrown when attempting to assign to an invalid field."""

    def __init__(self, message: str, dataclass: Any, field: str) -> None:
        """
        :param message:
            Human readable error message
        :param dataclass:
            :func:`dataclasses.dataclass` the :class:`DataclassBuilder` was made
            for.
        :param field:
            Name of the invalid field that the calling code tried to assign to.
        """
        super().__init__(message)
        self.dataclass = dataclass
        """:func:`dataclasses.dataclass` the :class:`DataclassBuilder` was made for."""
        self.field = field
        """Name of the invalid field that the calling code tried to assign to."""


class MissingFieldError(DataclassBuilderError):
    """Thrown when fields are missing when building a :func:`dataclasses.dataclass`."""

    def __init__(self, message: str, dataclass: Any, field: "Field[Any]") -> None:
        """
        :param message:
            Human readable error message
        :param dataclass:
            :func:`dataclasses.dataclass` the :class:`DataclassBuilder` was made for.
        :param field:
            The :class:`dataclasses.Field` representing the missing field that
            needs to be assigned.
        """
        super().__init__(message)
        self.dataclass = dataclass
        """:func:`dataclasses.dataclass` the :class:`DataclassBuilder` was made for."""
        self.field = field
        """
        The :class:`dataclasses.Field` representing the missing field that
        needs to be assigned.
        """

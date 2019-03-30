"""Common utilities.

.. _dataclass: https://docs.python.org/3/library/dataclasses.html
"""

import dataclasses
from typing import Any, Mapping

__all__ = ['REQUIRED', 'OPTIONAL', 'MISSING',
           '_is_settable', '_is_required', '_is_optional',
           '_settable_fields', '_required_fields', '_optional_fields']


class _RequiredType:
    """Type of constant to indicate that a field is required."""

    def __repr__(self) -> str:
        return 'REQUIRED'


class _OptionalType:
    """Type of constant to indicate that a field is optional."""

    def __repr__(self) -> str:
        return 'OPTIONAL'


class _MissingType:
    """Type of constant to indicate that a field is missing.

    Compares True with REQUIRED or OPTIONAL.

    """

    def __repr__(self) -> str:
        return 'MISSING'

    def __eq__(self, other: Any) -> bool:
        return other in (REQUIRED, OPTIONAL)

    def __ne__(self, other: Any) -> bool:
        return not self == other


REQUIRED = _RequiredType()

OPTIONAL = _OptionalType()

MISSING = _MissingType()


def _is_settable(field: 'dataclasses.Field[Any]') -> bool:
    """Determine if the given :class:`dataclasses.Field` is settable.

    Parameters
    ----------
    field
        Field to determine if it is settable.

    Returns
    -------
    bool
        True if the :paramref:`field` is optional, otherwise False.

    """
    return field.init


def _is_required(field: 'dataclasses.Field[Any]') -> bool:
    """Determine if the given :class:`dataclasses.Field` is required.

    Parameters
    ----------
    field
        Field to determine if it is required.

    Returns
    -------
    bool
        True if the :paramref:`field` is required, otherwise False.

    """
    return (field.init and field.default is dataclasses.MISSING and
            field.default_factory is dataclasses.MISSING)  # type: ignore


def _is_optional(field: 'dataclasses.Field[Any]') -> bool:
    """Determine if the given :class:`dataclasses.Field` is optional.

    Parameters
    ----------
    field
        Field to determine if it is optional.

    Returns
    -------
    bool
        True if the :paramref:`field` is optional, otherwise False.

    """
    return (field.init and
            (field.default is not dataclasses.MISSING) or
            (field.default_factory is not dataclasses.MISSING))  # type: ignore


def _settable_fields(dataclass: Any) -> Mapping[str, 'dataclasses.Field[Any]']:
    """Retrieve all settable fields from a dataclass_.

    Parameters
    ----------
    dataclass
        The dstaclass_ to get the settable fields for.

    Returns
    -------
    Mapping[str, Field[Any]]
        A dictionary of settable fields in the given :paramref:`dataclass`.
        The order will be the same as the order in the dataclass_.

    """
    return {field.name: field
            for field in dataclasses.fields(dataclass)
            if _is_settable(field)}


def _required_fields(dataclass: Any) -> Mapping[str, 'dataclasses.Field[Any]']:
    """Retrieve all required fields from a dataclass_.

    Parameters
    ----------
    dataclass
        The dstaclass_ to get the required fields for.

    Returns
    -------
    Mapping[str, Field[Any]]
        A dictionary of required fields in the given :paramref:`dataclass`.
        The order will be the same as the order in the dataclass_.

    """
    return {field.name: field
            for field in dataclasses.fields(dataclass)
            if _is_required(field)}


def _optional_fields(dataclass: Any) -> Mapping[str, 'dataclasses.Field[Any]']:
    """Retrieve all optional fields from a dataclass_.

    Parameters
    ----------
    dataclass
        The dstaclass_ to get the optional fields for.

    Returns
    -------
    Mapping[str, Field[Any]]
        A dictionary of optional fields in the given :paramref:`dataclass`.
        The order will be the same as the order in the dataclass_.

    """
    return {field.name: field
            for field in dataclasses.fields(dataclass)
            if _is_optional(field)}

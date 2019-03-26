"""Common utilities.

.. _dataclass: https://docs.python.org/3/library/dataclasses.html
"""

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Mapping
    from dataclasses import Field, fields, MISSING
else:
    from dataclasses import fields, MISSING

__all__ = ['_is_settable', '_is_required', '_is_optional',
           '_settable_fields', '_required_fields', '_optional_fields']


def _is_settable(field: 'Field[Any]') -> bool:
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


def _is_required(field: 'Field[Any]') -> bool:
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
    return (field.init and field.default == MISSING and
            field.default_factory == MISSING)  # type: ignore


def _is_optional(field: 'Field[Any]') -> bool:
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
            (field.default != MISSING or
             field.default_factory != MISSING))  # type: ignore


def _settable_fields(dataclass: Any) -> 'Mapping[str, Field[Any]]':
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
    return {f.name: f for f in fields(dataclass) if _is_settable(f)}


def _required_fields(dataclass: Any) -> 'Mapping[str, Field[Any]]':
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
    return {f.name: f for f in fields(dataclass) if _is_required(f)}


def _optional_fields(dataclass: Any) -> 'Mapping[str, Field[Any]]':
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
    return {f.name: f for f in fields(dataclass) if _is_optional(f)}

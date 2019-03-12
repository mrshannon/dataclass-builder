"""Utility functions for the package.

.. _dataclass: https://docs.python.org/3/library/dataclasses.html
"""

from typing import Any, TYPE_CHECKING

from .wrapper import DataclassBuilder

if TYPE_CHECKING:
    from typing import Mapping
    from dataclasses import Field

__all__ = ['build', 'fields']


def build(builder: DataclassBuilder) -> Any:
    """Use the given :class:`DataclassBuilder` to initialize a dataclass_.

    This will use the values assigned to the given :paramref:`builder` to
    construct a dataclass_ of the type the :paramref:`builder` was created for.

    .. note::

        This is not a method of :class:`DataclassBuilder` in order to not
        interfere with possible field names.  This function will use special
        private methods of :class:`DataclassBuilder` which are excepted from
        field assignment.

    Parameters
    ----------
    builder
        The dataclass builder to build from.

    Returns
    -------
    dataclass_
        An instance of the dataclass given in :func:`__init__` using the
        fields set on this builder.

    Raises
    ------
    MissingFieldError
        If not all of the required fields have been assigned to this
        builder.

    """
    # pylint: disable=protected-access
    return builder._build()


def fields(builder: DataclassBuilder, *,
           required: bool = True, optional: bool = True) \
        -> 'Mapping[str, Field[Any]]':
    """Get a dictionary of the given :class:`DataclassBuilder`'s fields.

    .. note::

        This is not a method of :class:`DataclassBuilder` in order to not
        interfere with possible field names.  This function will use special
        private methods of :class:`DataclassBuilder` which are excepted from
        field assignment.

    Parameters
    ----------
    builder
        The dataclass builder to get the fields for.
    required
        Set to False to not report required fields.
    optional
        Set to False to not report optional fields.

    Returns
    -------
    Mapping[str, 'dataclasses.Field[Any]']
        A mapping from field names to actual :class:`dataclasses.Field`'s
        in the same order as the :paramref:`builder`'s underlying
        dataclass_.

    """
    # pylint: disable=protected-access
    return builder._fields(required=required, optional=optional)

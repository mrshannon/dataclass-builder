"""Utility functions for the package."""

from typing import Any, TYPE_CHECKING

from .wrapper import DataclassBuilder

if TYPE_CHECKING:
    from typing import Mapping
    from dataclasses import Field

__all__ = ['build', 'fields']


def build(builder: DataclassBuilder) -> Any:
    """Use the given :class:`DataclassBuilder` to initialize a `dataclass`.

    This will use the values assigned to the given `builder` to construct a
    :func:`dataclasses.dataclass` of the type the `builder` was created for.

    .. note::

        This is not a method of :class:`DataclassBuilder` in order to not
        interfere with possible field names.  This function will use special
        private methods of :class:`DataclassBuilder` which are excepted from
        field assignment.

    :param builder:
        The dataclass builder to build from.

    :raises dataclass_builder.exceptions.MissingFieldError:
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

    :param builder:
        The dataclass builder to get the fields for.
    :param required:
        Set to False to not report required fields.
    :param optional:
        Set to False to not report optional fields.

    :return:
        A mapping from field names to actual :class:`dataclasses.Field`'s
        in the same order as the `builder`'s underlying
        :func:`dataclasses.dataclass`.

    """
    # pylint: disable=protected-access
    return builder._fields(required=required, optional=optional)

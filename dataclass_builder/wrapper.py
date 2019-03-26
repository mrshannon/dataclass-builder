"""Create instances of dataclasses with the builder pattern.

Examples
--------
Using a builder instance is the fastest way to get started with
`dataclass-builder`.

.. testcode::

    from dataclasses import dataclass
    from dataclass_builder import DataclassBuilder, build, fields

    @dataclass
    class Point:
        x: float
        y: float
        w: float = 1.0

Now we can build a point.

.. doctest::

    >>> p1_builder = DataclassBuilder(Point)
    >>> p1_builder.x = 5.8
    >>> p1_builder.y = 8.1
    >>> p1_builder.w = 2.0
    >>> build(p1_builder)
    Point(x=5.8, y=8.1, w=2.0)

Field values can also be provided in the constructor.

.. doctest::

    >>> p3_builder = DataclassBuilder(Point, w=100)
    >>> p3_builder.x = 5.8
    >>> p3_builder.y = 8.1
    >>> build(p3_builder)
    Point(x=5.8, y=8.1, w=100)

Fields with default values in the `dataclass` are optional in the builder.

.. doctest::

    >>> p4_builder = DataclassBuilder(Point)
    >>> p4_builder.x = 5.8
    >>> p4_builder.y = 8.1
    >>> build(p4_builder)
    Point(x=5.8, y=8.1, w=1.0)

Fields that don't have default values in the `dataclass` are not optional.

.. doctest::

    >>> p5_builder = DataclassBuilder(Point)
    >>> p5_builder.y = 8.1
    >>> build(p5_builder)
    Traceback (most recent call last):
    ...
    MissingFieldError: field 'x' of dataclass 'Point' is not optional

Fields not defined in the dataclass cannot be set in the builder.

.. doctest::

    >>> p6_builder = DataclassBuilder(Point)
    >>> p6_builder.z = 3.0
    Traceback (most recent call last):
    ...
    UndefinedFieldError: dataclass 'Point' does not define field 'z'

No exception will be raised for fields beginning with an underscore.

Accessing a field of the builder before it is set results in an
`AttributeError`.

.. doctest::

    >>> p8_builder = DataclassBuilder(Point)
    >>> p8_builder.x
    Traceback (most recent call last):
    ...
    AttributeError: 'DataclassBuilder' object has no attribute 'x'


.. _dataclass: https://docs.python.org/3/library/dataclasses.html
"""

import dataclasses
import itertools
from typing import Any, Mapping

from .exceptions import UndefinedFieldError, MissingFieldError
from ._common import _is_required

__all__ = ['DataclassBuilder']


class DataclassBuilder:
    """Wrap a dataclass_ with an object implementing the builder pattern.

    This class, via wrapping, allows dataclass_'s to be constructed with
    the builder pattern.  Once an instance is constructed simply assign to
    it's attributes, which are identical to the dataclass_ it was
    constructed with.  When done use the :func:`build` function to attempt
    to build the underlying dataclass_.

    .. warning::

        Because this class overrides attribute assignment when extending
        it care must be taken to only use private or "dunder" attributes
        and methods.

    Parameters
    ----------
    dataclass
        The dataclass_ that should be built by the
        builder instance
    **kwargs
        Optionally initialize fields during initialization of the builder.
        These can be changed later and will raise UndefinedFieldError if
        they are not part of the :paramref:`dataclass`'s `__init__` method.

    Raises
    ------
    TypeError
        If :paramref:`dataclass` is not a dataclass_.
        This is decided via :func:`dataclasses.is_dataclass`.
    UndefinedFieldError
        If you try to assign to a field that is not part of the
        :paramref:`dataclass`'s `__init__`.
    MissingFieldError
        If :func:`build` is called on this builder before all non default
        fields of the :paramref:`dataclass` are assigned.
    """

    def __init__(self, dataclass: Any, **kwargs: Any):
        if not dataclasses.is_dataclass(dataclass):
            raise TypeError("must be called with a dataclass type")
        self.__dataclass = dataclass
        fields_ = dataclasses.fields(self.__dataclass)
        self.__settable_fields = [
            field.name for field in fields_ if field.init]
        self.__required_fields = [
            field.name for field in fields_ if _is_required(field)]
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __setattr__(self, item: str, value: Any) -> None:
        """Set a field value, or an object attribute if it is private.

        .. note::

            This will pass through all attributes beginning with an underscore.
            If this is a valid field of the dataclass_ it will still be built
            correctly but UndefinedFieldError will not be thrown for attributes
            beginning with an underscore.

            If you need the exception to be thrown then set the field in the
            constructor.

        Parameters
        ----------
        item
            Name of the dataclass_ field or private/"dunder" attribute to set.
        value
            Value to assign to the dataclass_ field or private/"dunder"
            attribute.

        Raises
        ------
        UndefinedFieldError
            If :paramref:`item` is not initialisable in the underlying
            dataclass_.  If :paramref:`item` is private (begins with an
            underscore) or is a "dunder" then this exception will not
            be raised.

        """
        if item.startswith('_') or item in self.__settable_fields:
            self.__dict__[item] = value
        else:
            raise UndefinedFieldError(
                f"dataclass '{self.__dataclass.__name__}' does not define "
                f"field '{item}'", self.__dataclass, item)

    def __repr__(self) -> str:
        """Print a representation of the builder.

        Examples
        --------
        .. testcode::

            from dataclasses import dataclass
            from dataclass_builder import DataclassBuilder, build, fields

            @dataclass
            class Point:
                x: float
                y: float
                w: float = 1.0

        >>> DataclassBuilder(Point, x=4.0, w=2.0)
        DataclassBuilder(Point, x=4.0, w=2.0)

        Returns
        -------
            String representation that can be used to construct this builder
            instance.
        """
        args = itertools.chain(
            [self.__dataclass.__name__],
            (f'{item}={repr(getattr(self, item))}'
             for item in self.__settable_fields if hasattr(self, item)))
        return f"{self.__class__.__name__}({', '.join(args)})"

    def _build(self) -> Any:
        """Build the underlying dataclass_ using the fields from this builder.

        Returns
        -------
        dataclass
            An instance of the dataclass_ given in :func:`__init__` using the
            fields set on this builder instance.

        Raises
        ------
        MissingFieldError
            If not all of the required fields have been assigned to this
            builder instance.

        """
        for field in self.__required_fields:
            if field not in self.__dict__:
                raise MissingFieldError(
                    f"field '{field}' of dataclass "
                    f"'{self.__dataclass.__name__}' is not optional",
                    self.__dataclass, self._fields()[field])
        kwargs = {key: value
                  for key, value in self.__dict__.items()
                  if key in self.__settable_fields}
        return self.__dataclass(**kwargs)

    def _fields(self, required: bool = True, optional: bool = True) -> \
            Mapping[str, 'dataclasses.Field[Any]']:
        """Get a dictionary of the builder's fields.

        Parameters
        ----------
        required
            Set to False to not report required fields.
        optional
            Set to False to not report optional fields.

        Returns
        -------
        dict
            A mapping from field names to actual :class:`dataclasses.Field`'s
            in the same order as the underlying dataclass_.

        """
        if not required and not optional:
            return {}
        if required and not optional:
            return {field.name: field
                    for field in dataclasses.fields(self.__dataclass)
                    if field.name in self.__required_fields}
        if not required and optional:
            optional_fields = {name for name in self.__settable_fields
                               if name not in self.__required_fields}
            return {field.name: field
                    for field in dataclasses.fields(self.__dataclass)
                    if field.name in optional_fields}
        return {field.name: field
                for field in dataclasses.fields(self.__dataclass)
                if field.name in self.__settable_fields}

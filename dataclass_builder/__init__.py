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

__version__ = '0.0.2a1'

__all__ = ['DataclassBuilderError', 'UndefinedFieldError', 'MissingFieldError',
           'DataclassBuilder', 'build', 'fields']


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

    def __init__(self, message: str, dataclass: Any,
                 field: 'dataclasses.Field[Any]') -> None:
        super().__init__(message)
        self.dataclass = dataclass
        self.field = field


class DataclassBuilder:
    """Wrap a dataclass_ with an object implementing the builder pattern.

    This class, via wrapping, allows dataclass_'s to be constructed with
    the builder pattern.  Once an instance is constructed simply assign to
    it's attributes, which are identical to the dataclass_ it was
    constructed with.  When done use the :func:`build` function to attempt
    to build the underlying dataclass_.

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
            field.name for field in fields_ if _isrequired(field)]
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __setattr__(self, item: str, value: Any) -> None:
        """Set a field value, or an object attribute if "dunder".

        Parameters
        ----------
        item
            Name of the dataclass_ field or "dunder" to set.
        value
            Value to assign to the dataclass_ field or "dunder".

        Raises
        ------
        UndefinedFieldError
            If :paramref:`item` is not initialisable in the underlying
            dataclass_.  If :paramref:`item` is a "dunder" then this
            exception will not be raised.
        """
        if item.startswith('_' + self.__class__.__name__):
            self.__dict__[item] = value
        elif item not in self.__settable_fields:
            raise UndefinedFieldError(
                f"dataclass '{self.__dataclass.__name__}' does not define "
                f"field '{item}'", self.__dataclass, item)
        else:
            self.__dict__[item] = value

    def __repr__(self) -> str:
        """Print a representation of the builder.

        >>> DataclassBuilder(Point, x=4.0, w=2.0)
        DataclassBuilder(Point, x=4.0, w=2.0)

        Returns
        -------
            String representation that can be used to construct this builder.
        """
        args = itertools.chain(
            [self.__dataclass.__name__],
            (f'{item}={getattr(self, item)}'
             for item in self.__settable_fields if hasattr(self, item)))
        return f"{self.__class__.__name__}({', '.join(args)})"

    def __build(self) -> Any:
        """Build the underlying dataclass_ using the fields from this builder.

        Returns
        -------
        dataclass
            An instance of the dataclass_ given in :func:`__init__` using the
            fields set on this builder.

        Raises
        ------
        MissingFieldError
            If not all of the required fields have been assigned to this
            builder.

        """
        for field in self.__required_fields:
            if field not in self.__dict__:
                raise MissingFieldError(
                    f"field '{field}' of dataclass "
                    f"'{self.__dataclass.__name__}' is not optional",
                    self.__dataclass, self.__fields()[field])
        kwargs = {key: value
                  for key, value in self.__dict__.items()
                  if key in self.__settable_fields}
        return self.__dataclass(**kwargs)

    def __fields(self, required: bool = True, optional: bool = True) -> \
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


def build(builder: DataclassBuilder) -> Any:
    """Use the given :class:`DataclassBuilder` to initialize a dataclass_.

    This will use the values assigned to the given :paramref:`builder` to
    construct a dataclass_ of the type the :paramref:`builder` was created for.

    .. note::

        This is not a method of :class:`DataclassBuilder` in order to not
        interfere with possible field names.  This function will use special
        "dunder" methods of :class:`DataclassBuilder` which are excepted from
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
    return getattr(builder, f'_{builder.__class__.__name__}__build')()


def fields(builder: DataclassBuilder, *,
           required: bool = True, optional: bool = True) \
        -> Mapping[str, 'dataclasses.Field[Any]']:
    """Get a dictionary of the given :class:`DataclassBuilder`'s fields.

    .. note::

        This is not a method of :class:`DataclassBuilder` in order to not
        interfere with possible field names.  This function will use special
        "dunder" methods of :class:`DataclassBuilder` which are excepted from
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
    fields_method = getattr(builder, f'_{builder.__class__.__name__}__fields')
    fields_: Mapping[str, 'dataclasses.Field[Any]'] = fields_method(
        required=required, optional=optional)
    return fields_


def _isrequired(field: 'dataclasses.Field[Any]') -> bool:
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
    return (field.init and field.default == dataclasses.MISSING and
            field.default_factory == dataclasses.MISSING)  # type: ignore

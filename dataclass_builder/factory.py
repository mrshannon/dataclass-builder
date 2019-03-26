"""Create dataclass_ builders for specific dataclasses.

Examples
--------
Using specialized builders allows for better documentation and type checking
than using generic builders.

.. testcode::

    from dataclasses import dataclass
    from dataclass_builder import dataclass_builder, REQUIRED, OPTIONAL

    @dataclass
    class Point:
        x: float
        y: float
        w: float = 1.0

    PointBuilder = dataclass_builder(Point)

Now we can build a point.

.. doctest::

    >>> builder = PointBuilder()
    >>> builder.x = 5.8
    >>> builder.y = 8.1
    >>> builder.w = 2.0
    >>> builder.build()
    Point(x=5.8, y=8.1, w=2.0)

Field values can also be provided in the constructor.

.. doctest::

    >>> builder = PointBuilder(w=100)
    >>> builder.x = 5.8
    >>> builder.y = 8.1
    >>> builder.build()
    Point(x=5.8, y=8.1, w=100)

Fields with default values in the `dataclass` are optional in the builder.

.. doctest::

    >>> builder = PointBuilder()
    >>> builder.x = 5.8
    >>> builder.y = 8.1
    >>> builder.build()
    Point(x=5.8, y=8.1, w=1.0)

Fields that don't have default values in the `dataclass` are not optional.

.. doctest::

    >>> builder = PointBuilder()
    >>> builder.y = 8.1
    >>> builder.build()
    Traceback (most recent call last):
    ...
    MissingFieldError: field 'x' of dataclass 'Point' is not optional

Fields not defined in the dataclass cannot be set in the builder.

.. doctest::

    >>> builder = PointBuilder()
    >>> builder.z = 3.0
    Traceback (most recent call last):
    ...
    UndefinedFieldError: dataclass 'Point' does not define field 'z'

No exception will be raised for fields beginning with an underscore.

Accessing a field of the builder before it is set gives either the `REQUIRED`
or `OPTIONAL` constant

.. doctest::

    >>> builder = PointBuilder()
    >>> builder.x
    REQUIRED

.. doctest::

    >>> builder = PointBuilder()
    >>> builder.w
    OPTIONAL


.. note::

    If one of the initialisable fields of the dataclass is `build` or `fields`
    the functional versions instead of the method versions must be used.


.. _dataclass: https://docs.python.org/3/library/dataclasses.html

"""

from typing import (Any, Callable, Dict, Mapping, MutableMapping, Optional,
                    Sequence, TYPE_CHECKING, cast)

from ._common import (REQUIRED, OPTIONAL, _is_required,
                      _settable_fields, _required_fields, _optional_fields)
from .exceptions import UndefinedFieldError, MissingFieldError

if TYPE_CHECKING:
    from dataclasses import Field, is_dataclass
else:
    from dataclasses import is_dataclass

__all__ = ['dataclass_builder']


class _MissingType:
    def __repr__(self) -> str:
        return 'MISSING'


_MISSING = _MissingType()


# copied (and modified) from dataclasses._create_fn to avoid dependency on
# private functions in dataclasses
def _create_fn(name: str, args: Sequence[str], body: Sequence[str],
               env: Optional[Dict[str, Any]] = None, *,
               return_type: Any = _MISSING) \
        -> Callable[..., Any]:
    locals_: MutableMapping[str, Any] = {}
    return_annotation = ''
    if env is None:
        env = {}
    if return_type is not _MISSING:
        env['_return_type'] = return_type
        return_annotation = '->_return_type'
    args = ', '.join(args)
    body = '\n'.join(f' {line}' for line in body)
    txt = f'def {name}({args}){return_annotation}:\n{body}'
    # this is how the dataclasses module makes custom methods so it's good
    # enough for this package
    exec(txt, env, locals_)  # pylint: disable=exec-used
    return cast(Callable[..., Any], locals_[name])


def _create_init_method(fields: Mapping[str, 'Field[Any]']) \
        -> Callable[..., None]:
    env: Dict[str, Any] = {
        f'_{name}_type': field.type for name, field in fields.items()}
    env['REQUIRED'] = REQUIRED
    env['OPTIONAL'] = OPTIONAL

    def is_required(field: 'Field[Any]') -> str:
        return 'REQUIRED' if _is_required(field) else 'OPTIONAL'

    args = ['self'] + [f'{name}: _{name}_type = {is_required(field)}'
                       for name, field in fields.items()]
    body = [f'self.{name}: _{name}_type = {name}' for name in fields]
    body = ['self.__initialized = False'] + body + [
        'self.__initialized = True']
    return _create_fn('__init__', args, body, env, return_type=None)


def dataclass_builder(dataclass: Any, *, name: Optional[str] = None) -> Any:
    """Create a new builder class that is specialized to the given dataclass_.

    Parameters
    ----------
    dataclass
        The dataclass_ to create the builder for.
    name
        Override the name of the builder, by default it will be
        '<dataclass>Builder' where <dataclass> is replaced by the name of the
        dataclass.

    Returns
    -------
    object
        A new dataclass builder class that is specialized to the given
        :paramref:`dataclass`.  If the given dataclass_ does not contain the
        fields `build` or `fields` these will be exposed as public methods with
        the same signature as the :func:`dataclass_builder.utility.build` and
        :func:`dataclass_builder.utility.fields` functions.

    Raises
    ------
    TypeError
        If :paramref:`dataclass` is not a dataclass_.
        This is decided via :func:`dataclasses.is_dataclass`.

    """
    if not is_dataclass(dataclass):
        raise TypeError("must be called with a dataclass type")

    settable_fields = _settable_fields(dataclass)
    required_fields = _required_fields(dataclass)
    optional_fields = _optional_fields(dataclass)

    # validate identifiers
    for field in _settable_fields(dataclass):
        # there should not be anyway to trigger this branch
        if not field.isidentifier():  # pragma: no cover
            raise RuntimeError(
                f"field name '{field}'' could cause a security issue, refusing"
                f" to construct builder for '{dataclass.__qualname__}'")

    def _setattr_method(self: Any, name: str, value: Any) -> None:
        """Set a field value, or an object attribute if it is private.

        .. note::

            This will pass through all attributes beginning with an underscore.
            If this is a valid field of the dataclass_ it will still be built
            correction but UndefinedFieldError will not be thrown for
            attributes beginning with an underscore.

            If you need the exception to be thrown then set the field in the
            constructor.

        Parameters
        ----------
        name
            Name of the dataclass_ field or private/"dunder" attribute to set.
        value
            Value to assign to the dataclass_ field or private/"dunder"
            attribute.

        Raises
        ------
        UndefinedFieldError
            If :paramref:`name` is not initialisable in the underlying
            dataclass_.  If :paramref:`name` is private (begins with an
            underscore) or is a "dunder" then this exception will not
            be raised.

        """
        # self.__initialized is not protected member access, since this is
        # a class method
        if (name.startswith('_') or hasattr(self, name) or
                not self.__initialized):  # pylint: disable=protected-access
            object.__setattr__(self, name, value)
        else:
            raise UndefinedFieldError(
                f"dataclass '{dataclass.__qualname__}' does not define "
                f"field '{name}'", dataclass, name)

    def _repr_method(self: Any) -> str:
        """Print a representation of the builder.

        Examples
        --------
        >>> PointBuilder = dataclass_builder(Point)
        >>> PointBuilder(x=4.0, w=2.0)
        PointBuilder(x=4.0, w=2.0)

        Returns
        -------
            String representation that can be used to construct this builder
            instance.
        """
        args = []
        for name in settable_fields:
            value = getattr(self, name)
            if value not in (REQUIRED, OPTIONAL):
                args.append(f'{name}={repr(value)}')
        return f'{self.__class__.__qualname__}({", ".join(args)})'

    def _build_method(self: Any) -> Any:
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
        # check for missing required fields
        for name, field in required_fields.items():
            if getattr(self, name) == REQUIRED:
                raise MissingFieldError(
                    f"field '{name}' of dataclass '{dataclass.__qualname__}' "
                    "is not optional", dataclass, field)
        # build dataclass
        kwargs = {name: getattr(self, name)
                  for name in settable_fields
                  if getattr(self, name) != OPTIONAL}
        return dataclass(**kwargs)

    def _fields_method(
            _: Any, required: bool = True, optional: bool = True) \
            -> Mapping[str, 'Field[Any]']:
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
            return required_fields
        if not required and optional:
            return optional_fields
        return settable_fields

    # assemble new builder class methods
    dict_: Dict[str, Any] = dict()
    dict_['__init__'] = _create_init_method(settable_fields)
    dict_['__setattr__'] = _setattr_method
    dict_['__repr__'] = _repr_method
    dict_['_build'] = _build_method
    dict_['_fields'] = _fields_method

    # add default docstring
    dname = dataclass.__qualname__
    params = '\n'.join([
        f'    {name} : {field.type.__name__}\n        '
        f'Optionally initialize `{name}` field.\n'
        for name, field in settable_fields.items()])
    dict_['__doc__'] = (
        f"""Builder for the {dname} dataclass_.

    This class allows the {dname} dataclass_ to be constructed with the
    builder pattern.  Once an instance is constructed simply assign to
    it's attributes, which are identical to the {dname} dataclass_.  When
    done use it's `build` method, or the :func:`build` function if one of
    the fields is `build`, to make an instance of the {dname} dataclass_
    using the field values set on this builder.

    .. warning::

        Because this class overrides attribute assignment when extending
        it care must be taken to only use private or "dunder" attributes
        and methods.

    Parameters
    ----------
{params}

    Raises
    ------
    UndefinedFieldError
        If you try to assign to a field that is not part of the
        :paramref:`dataclass`'s `__init__`.
    MissingFieldError
        If :func:`build` is called on this builder before all non default
        fields of the :paramref:`dataclass` are assigned.

        """)

    if 'build' not in settable_fields:
        dict_['build'] = _build_method

    if 'build' not in settable_fields:
        dict_['fields'] = _fields_method

    if name is None:
        name = f'{dataclass.__name__}Builder'

    return type(name, (object,), dict_)

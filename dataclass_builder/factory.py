from typing import (Any, Optional, Sequence, Dict, Callable, Mapping,
                    cast, TYPE_CHECKING)

from .exceptions import UndefinedFieldError, MissingFieldError
from ._common import (_settable_fields, _required_fields, _optional_fields,
                      _is_required)

if TYPE_CHECKING:
    from dataclasses import Field

__all__ = ['dataclass_builder', 'REQUIRED', 'OPTIONAL']


class MISSING_TYPE:
    pass


class REQUIRED_TYPE:
    pass


class OPTIONAL_TYPE:
    pass


MISSING = MISSING_TYPE()

REQUIRED = REQUIRED_TYPE()

OPTIONAL = OPTIONAL_TYPE()


# copied (and modified) from dataclasses._create_fn to avoid dependency on
# private functions in dataclasses
def _create_fn(name: str, args: Sequence[str], body: Sequence[str],
               env: Optional[Dict[str, Any]] = None, *,
               return_type: Any = MISSING) \
        -> Callable[..., Any]:
    locals = {}
    return_annotation = ''
    if return_type is not MISSING:
        env['_return_type'] = return_type
        return_annotation = '->_return_type'
    args = ', '.join(args)
    body = '\n'.join(f' {line}' for line in body)
    txt = f'def {name}({args}){return_annotation}:\n{body}'
    exec(txt, env, locals)
    return cast(Callable[..., Any], locals[name])


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
    body = ['self.__initialized = False'] + body + ['self.__initialized = True']
    return _create_fn('__init__', args, body, env, return_type=None)


def dataclass_builder(dataclass: Any, *, name: Optional[str] = None) -> Any:

    settable_fields = _settable_fields(dataclass)

    # validate identifiers
    for field in settable_fields:
        if not field.isidentifier():
            raise RuntimeError(
                f"field name '{field}'' could cause a security issue, refusing "
                f"to construct builder for '{dataclass.__qualname__}'")

    def _setattr_method(self: Any, name: str, value: Any) -> None:
        if (name.startswith('_') or hasattr(self, name) or
                not self.__initialized):
            object.__setattr__(self, name, value)
        else:
            raise UndefinedFieldError(
                f"dataclass '{dataclass.__qualname__}' does not define "
                f"field '{name}'", dataclass, name)

    def _repr_method(self: Any) -> str:
        args = []
        for name in settable_fields:
            value = getattr(self, name)
            if value != REQUIRED and value != OPTIONAL:
                args.append(f'{name}={repr(value)}')
        return f'{self.__class__.__qualname__}({", ".join(args)})'

    def _build_method(self: Any) -> Any:
        # check for missing required fields
        for name, field in _required_fields(dataclass).items():
            if getattr(self, name) == REQUIRED:
                raise MissingFieldError(
                    f"field '{name}' of dataclass '{dataclass.__qualname__}' "
                    "is not optional", dataclass, field)
        # build dataclass
        kwargs = {name: getattr(self, name)
                  for name in _settable_fields(dataclass)
                  if getattr(self, name) != OPTIONAL}
        return dataclass(**kwargs)

    def _fields_method(self, required: bool = True, optional: bool = True) \
            -> Mapping[str, 'Field[Any]']:
        if not required and not optional:
            return {}
        if required and not optional:
            return _required_fields(dataclass)
        if not required and optional:
            return _optional_fields(dataclass)
        return _settable_fields(dataclass)

    # assemble new builder class
    dict_: Dict[str, Any] = dict()
    dict_['__init__'] = _create_init_method(settable_fields)
    dict_['__setattr__'] = _setattr_method
    dict_['__repr__'] = _repr_method
    dict_['_build'] = _build_method
    dict_['_fields'] = _fields_method

    if 'build' not in settable_fields:
        dict_['build'] = _build_method

    if 'build' not in settable_fields:
        dict_['fields'] = _fields_method

    if name is None:
        name = f'{dataclass.__name__}Builder'

    return type(name, (object,), dict_)

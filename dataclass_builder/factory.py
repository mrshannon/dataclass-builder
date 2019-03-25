from typing import Any, Optional, Sequence, Dict, Callable, Mapping, cast, TYPE_CHECKING

from ._common import _required_fields, _settable_fields, _optional_fields, _is_required
from .exceptions import UndefinedFieldError, MissingFieldError

if TYPE_CHECKING:
    from dataclasses import Field

__all__ = ['dataclass_builder']


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
    # print('\n\n' + txt)
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


def _create_repr_method(fields: Mapping[str, 'Field[Any]']) \
        -> Callable[..., str]:
    env = {'REQUIRED': REQUIRED, 'OPTIONAL': OPTIONAL}
    args = ['self']
    body = ['args = []']
    for field in fields:
        body.append(
            f'if self.{field} != REQUIRED and self.{field} != OPTIONAL:')
        body.append(f' args.append(f"{field}={{repr(self.{field})}}")')
    body.append('args = ", ".join(args)')
    body.append('return f"{self.__class__.__qualname__}({args})"')
    return _create_fn('__repr__', args, body, env, return_type=str)


def _build_method(self: Any):
    return self._build()


def _create_build_method(dataclass: Any) -> Callable[..., Any]:
    env = {'dataclass': dataclass,
           'REQUIRED': REQUIRED,
           'OPTIONAL': OPTIONAL,
           'settable_fields': _settable_fields,
           'MissingFieldError': MissingFieldError}
    args = ['self']
    body = []

    # check for missing required fields
    for name, field in _required_fields(dataclass).items():
        body.append(f'if self.{name} == REQUIRED:')
        txt = (f"field '{name}' of dataclass '{dataclass.__qualname__}'"
               " is not optional")
        body.append(f' raise MissingFieldError("{txt}", dataclass, '
                    f'settable_fields(dataclass)["{name}"])')

    # build dataclass
    required = (
        f'"{name}": self.{name}' for name in _required_fields(dataclass))
    body.append(f'kwargs = {{{", ".join(required)}}}')
    for name in _optional_fields(dataclass):
        body.append(f'if self.{name} != REQUIRED and self.{name} != OPTIONAL:')
        body.append(f' kwargs["{name}"] = self.{name}')
    body.append('return dataclass(**kwargs)')

    return _create_fn('_build', args, body, env, return_type=str)


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

    dict_: Dict[str, Any] = dict()
    dict_['__init__'] = _create_init_method(settable_fields)
    dict_['__setattr__'] = _setattr_method
    dict_['__repr__'] = _create_repr_method(settable_fields)
    dict_['_build'] = _create_build_method(dataclass)

    if 'build' not in settable_fields:
        dict_['build'] = _build_method

    if name is None:
        name = f'{dataclass.__name__}Builder'

    return type(name, (object,), dict_)

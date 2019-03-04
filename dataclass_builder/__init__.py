"""Create instances of dataclasses with the builder pattern."""

import inspect
import itertools
from dataclasses import Field, _MISSING_TYPE, _FIELDS
from typing import Any, Mapping, MutableMapping, Iterator

__version__ = '0.0.1a1'

__all__ = ['DataclassBuilderError', 'UndefinedFieldError', 'MissingFieldError',
           'DataclassBuilder', 'build', 'fields']


class DataclassBuilderError(Exception):
    pass


class UndefinedFieldError(DataclassBuilderError):

    def __init__(self, message: str, dataclass: Any, field: str) -> None:
        super().__init__(message)
        self.dataclass = dataclass
        self.field = field


class MissingFieldError(DataclassBuilderError):

    def __init__(self, message: str, dataclass: Any, field: 'Field[Any]') \
            -> None:
        super().__init__(message)
        self.dataclass = dataclass
        self.field = field


class DataclassBuilder(MutableMapping[str, Any]):

    def __init__(self, dataclass: Any, **kwargs: Any):
        assert inspect.isclass(dataclass)
        assert hasattr(dataclass, _FIELDS)
        self.__dataclass = dataclass
        fields_ = getattr(self.__dataclass, _FIELDS).items()
        self.__fields = {
            name: field.type for name, field in fields_ if field.init}
        self.__required_fields = {
            name: field.type for name, field in fields_ if _isrequired(field)}
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __getitem__(self, key: str) -> Any:
        if key in self.__fields and hasattr(self, key):
            return getattr(self, key)
        raise KeyError(repr(key))

    def __setitem__(self, key: str, value: Any) -> None:
        if key in self.__fields:
            self.__dict__[key] = value

    def __delitem__(self, key: str) -> None:
        if key in self.__fields:
            del self.__dict__[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self.__fields)

    def __len__(self) -> int:
        return len(self.__fields)

    def __setattr__(self, item: str, value: Any) -> None:
        if item.startswith('_' + self.__class__.__name__):
            self.__dict__[item] = value
        elif item not in self.__fields:
            raise UndefinedFieldError(
                f"dataclass '{self.__dataclass.__name__}' does not define "
                f"field '{item}'", self.__dataclass, item)
        else:
            self.__dict__[item] = value

    def __repr__(self) -> str:
        args = itertools.chain(
            [self.__dataclass.__name__],
            (f'{key}={self[key]}' for key in self.__fields if key in self))
        return f"{self.__class__.__name__}({', '.join(args)})"

    def __build(self) -> Any:
        kwargs = {key: value
                  for key, value in self.__dict__.items()
                  if key in self.__fields}
        try:
            return self.__dataclass(**kwargs)
        except TypeError:
            for field in self.__required_fields:
                if field not in self.__dict__:
                    raise MissingFieldError(
                        f"field '{field}' of dataclass "
                        f"'{self.__dataclass.__name__}' is not optional",
                        self.__dataclass, field)


def build(builder: DataclassBuilder) -> Any:
    return getattr(builder, f'_{builder.__class__.__name__}__build')()


def fields(builder: DataclassBuilder, *,
           required: bool = True, optional: bool = True) \
        -> Mapping[str, 'Field[Any]']:
    if required and optional:
        fields_ = getattr(builder, f'_{builder.__class__.__name__}__fields')
    elif required:
        fields_ = getattr(
            builder, f'_{builder.__class__.__name__}__required_fields')
    else:
        fields_ = getattr(
            builder, f'_{builder.__class__.__name__}__optional_fields')
    return {field.name: field.type for field in fields_.values()}


def _isrequired(field: 'Field[Any]') -> bool:
    return field.init and isinstance(field.default, _MISSING_TYPE) and \
           isinstance(field.default_factory, _MISSING_TYPE)  # type: ignore

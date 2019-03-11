"""Create instances of dataclasses with the builder pattern."""

import itertools
import dataclasses
from typing import Any, Mapping

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

    def __init__(self, message: str, dataclass: Any, field: str) -> None:
        super().__init__(message)
        self.dataclass = dataclass
        self.field = field


class DataclassBuilder:

    def __init__(self, dataclass: Any, **kwargs: Any):
        if not dataclasses.is_dataclass(dataclass):
            raise TypeError("must be called with a dataclass type")
        self.__dataclass = dataclass
        fields_ = dataclasses.fields(self.__dataclass)
        self.__fields = [field.name for field in fields_ if field.init]
        self.__required_fields = {
            field.name for field in fields_ if _isrequired(field)}
        for key, value in kwargs.items():
            setattr(self, key, value)

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
            (f'{item}={getattr(self, item)}'
             for item in self.__fields if hasattr(self, item)))
        return f"{self.__class__.__name__}({', '.join(args)})"

    def __build(self) -> Any:
        for field in self.__required_fields:
            if field not in self.__dict__:
                raise MissingFieldError(
                    f"field '{field}' of dataclass "
                    f"'{self.__dataclass.__name__}' is not optional",
                    self.__dataclass, field)
        kwargs = {key: value
                  for key, value in self.__dict__.items()
                  if key in self.__fields}
        return self.__dataclass(**kwargs)


def build(builder: DataclassBuilder) -> Any:
    return getattr(builder, f'_{builder.__class__.__name__}__build')()


def fields(builder: DataclassBuilder, *,
           required: bool = True, optional: bool = True) \
        -> Mapping[str, 'dataclasses.Field[Any]']:
    if required and optional:
        fields_ = getattr(builder, f'_{builder.__class__.__name__}__fields')
    elif required:
        fields_ = getattr(
            builder, f'_{builder.__class__.__name__}__required_fields')
    else:
        fields_ = getattr(
            builder, f'_{builder.__class__.__name__}__optional_fields')
    return {field.name: field.type for field in fields_.values()}


def _isrequired(field: 'dataclasses.Field[Any]') -> bool:
    return field.init and field.default == dataclasses.MISSING and \
           field.default_factory == dataclasses.MISSING  # type: ignore

"""Create instances of dataclasses with the builder pattern."""

import inspect
import itertools
from dataclasses import Field, _MISSING_TYPE, _FIELDS
from typing import Any, Mapping, MutableMapping, Iterator

from cached_property import cached_property  # type: ignore

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
        # any class that has a _FIELDS attribute is considered a dataclass
        assert inspect.isclass(dataclass)
        assert hasattr(dataclass, _FIELDS)
        self.__dataclass = dataclass
        self.__dataclass_attributes: MutableMapping[str, Any] = dict()
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __getitem__(self, key: str) -> Any:
        return self.__dataclass_attributes[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.__dataclass_attributes[key] = value

    def __delitem__(self, key: str) -> None:
        del self.__dataclass_attributes[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self.__dataclass_attributes)

    def __len__(self) -> int:
        return len(self.__dataclass_attributes)

    def __getattr__(self, item: str) -> Any:
        try:
            return self.__dataclass_attributes[item]
        except KeyError:
            raise AttributeError(
                f"'{self.__class__.__name__}({self.__dataclass.__name__})' "
                f"object has no attribute '{item}'")

    def __setattr__(self, item: str, value: Any) -> None:
        if item.startswith('_' + self.__class__.__name__):
            self.__dict__[item] = value
        elif item not in self.__fields:
            raise UndefinedFieldError(
                f"dataclass '{self.__dataclass.__name__}' does not define "
                f"field '{item}'", self.__dataclass, item)
        else:
            self.__dataclass_attributes[item] = value

    def __delattr__(self, item: str) -> None:
        if item.startswith('_' + self.__class__.__name__):
            del self.__dict__[item]
        else:
            del self.__dataclass_attributes[item]

    def __repr__(self) -> str:
        args = itertools.chain(
            [self.__dataclass.__name__],
            (f'{key}={self.__dataclass_attributes[key]}'
             for key in getattr(self.__dataclass, _FIELDS)
             if key in self.__dataclass_attributes))
        return f"{self.__class__.__name__}({', '.join(args)})"

    def __build(self) -> Any:
        kwargs = {key: value
                  for key, value in self.__dataclass_attributes.items()
                  if key in self.__fields}
        try:
            return self.__dataclass(**kwargs)
        except TypeError:
            for field in self.__required_fields.values():
                if field.name not in self.__dataclass_attributes:
                    raise MissingFieldError(
                        f"field '{field.name}' of dataclass "
                        f"'{self.__dataclass.__name__}' is not optional",
                        self.__dataclass, field)

    @cached_property
    def __fields(self) -> Mapping[str, 'Field[Any]']:
        return {**self.__required_fields, **self.__optional_fields}

    @cached_property
    def __required_fields(self) -> Mapping[str, 'Field[Any]']:
        return {name: field
                for name, field in
                getattr(self.__dataclass, _FIELDS).items()
                if _isrequired(field)}

    @cached_property
    def __optional_fields(self) -> Mapping[str, 'Field[Any]']:
        return {name: field
                for name, field in
                getattr(self.__dataclass, _FIELDS).items()
                if field.init and not _isrequired(field)}


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

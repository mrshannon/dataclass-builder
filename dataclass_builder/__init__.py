"""Create instances of dataclasses with the builder pattern.

.. _dataclass: https://docs.python.org/3/library/dataclasses.html
"""

from .exceptions import (DataclassBuilderError, UndefinedFieldError,
                         MissingFieldError)
from .wrapper import DataclassBuilder
from .factory import dataclass_builder, REQUIRED, OPTIONAL
from .utility import build, fields

__version__ = '0.0.3'

__all__ = ['DataclassBuilderError', 'UndefinedFieldError', 'MissingFieldError',
           'DataclassBuilder', 'REQUIRED', 'OPTIONAL',
           'dataclass_builder', 'build', 'fields']

"""Create instances of dataclasses with the builder pattern.

.. _dataclass: https://docs.python.org/3/library/dataclasses.html
"""

from .exceptions import (DataclassBuilderError, UndefinedFieldError,
                         MissingFieldError)
from .wrapper import DataclassBuilder
from .factory import dataclass_builder
from .utility import build, fields
from ._common import REQUIRED, OPTIONAL, MISSING

__version__ = '1.1.3'

__all__ = ['DataclassBuilderError', 'UndefinedFieldError', 'MissingFieldError',
           'DataclassBuilder', 'REQUIRED', 'OPTIONAL', 'MISSING',
           'dataclass_builder', 'build', 'fields']

"""Create instances of dataclasses with the builder pattern.

.. _dataclass: https://docs.python.org/3/library/dataclasses.html
"""

from ._common import MISSING, OPTIONAL, REQUIRED
from .exceptions import DataclassBuilderError, MissingFieldError, UndefinedFieldError
from .factory import dataclass_builder
from .utility import build, fields
from .wrapper import DataclassBuilder

__version__ = '1.1.3'

__all__ = ['DataclassBuilderError', 'UndefinedFieldError', 'MissingFieldError',
           'DataclassBuilder', 'REQUIRED', 'OPTIONAL', 'MISSING',
           'dataclass_builder', 'build', 'fields']

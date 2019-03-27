"""Create instances of dataclasses with the builder pattern.

.. _dataclass: https://docs.python.org/3/library/dataclasses.html
"""

from .exceptions import (DataclassBuilderError, UndefinedFieldError,
                         MissingFieldError)
from .wrapper import DataclassBuilder
from .factory import dataclass_builder
from .utility import build, fields
from ._common import REQUIRED, OPTIONAL

__version__ = '1.0.1'

__all__ = ['DataclassBuilderError', 'UndefinedFieldError', 'MissingFieldError',
           'DataclassBuilder', 'REQUIRED', 'OPTIONAL',
           'dataclass_builder', 'build', 'fields']

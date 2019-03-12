"""Create instances of dataclasses with the builder pattern.

.. _dataclass: https://docs.python.org/3/library/dataclasses.html
"""

from .exceptions import (DataclassBuilderError, UndefinedFieldError,
                         MissingFieldError)
from .wrapper import DataclassBuilder
from .utility import build, fields

__version__ = '0.0.2a1'

__all__ = ['DataclassBuilderError', 'UndefinedFieldError', 'MissingFieldError',
           'DataclassBuilder', 'build', 'fields']

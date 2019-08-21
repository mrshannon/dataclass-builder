"""Create instances of dataclasses with the builder pattern.

.. _dataclass: https://docs.python.org/3/library/dataclasses.html
"""

from .__version__ import __version__
from ._common import MISSING, OPTIONAL, REQUIRED
from .exceptions import DataclassBuilderError, MissingFieldError, UndefinedFieldError
from .factory import dataclass_builder
from .utility import build, fields, update
from .wrapper import DataclassBuilder

__all__ = [
    "__version__",
    "DataclassBuilderError",
    "UndefinedFieldError",
    "MissingFieldError",
    "DataclassBuilder",
    "REQUIRED",
    "OPTIONAL",
    "MISSING",
    "dataclass_builder",
    "build",
    "fields",
    "update",
]

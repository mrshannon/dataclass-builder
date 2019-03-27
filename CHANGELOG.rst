Changelog
=========


Unreleased_
-----------

**BREAKS BACKWARDS COMPATIBILITY**

* Moved :code:`REQUIRED` and :code:`OPTIONAL` constants into :code:`._common`
  with exports at the package level.
* Fixed bug in :code:`DataclassBuilder.__repr__` causing some types of fields
  such as strings to not display properly.
* Rewrite :code:`DataclassBuilder` to share functions with the factory
  version :code:`dataclass_builder`.
* Change how :code:`DataclassBuilder` handles unset fields so that they will
  be initialized to :code:`REQUIRED` and :code:`OPTIONAL` in order to be
  compatible with the classes returned from the :code:`dataclass_builder`
  factory.
* Fields passed in the :code:`__init__` method of :code:`DataclassBuilder` will
  now raise :code:`TypeError` (instead of :code:`UndefinedFieldError`) the same
  as classes build with the :code:`dataclass_builder` factory.
* Disabled positional arguments for builders generated with the
  :code:`dataclass_builder` factory.


v0.0.3_ - 2019-03-26
--------------------

* Added :code:`.factory.dataclass_builder` factory function to create builder
  classes for specific dataclasses.
* Moved :code:`build` and :code:`fields` functions to the :code:`.utility`
  submodule with exports at the top level.
* Moved :code:`DataclassBuilder` to the :code:`.wrapper` submodule with exports
  at the top level.
* Fixed issue #4 which caused typing errors in code using
  :code:`DataclassBuilder`.


v0.0.2_ - 2019-03-12
--------------------

* Added additional unit tests.
* Fixed issue #1 preventing :code:`DataclassBuilder` from being subclassed.
* Fields beginning with an underscore will no longer be checked.


v0.0.1 - 2019-03-11
-------------------

* Added :code:`DataclassBuilder` class to wrap Python dataclasses_ with a
  factory implementing the builder pattern.
* Added :code:`build` function to construct a dataclass_ from a
  :code:`DataclassBuilder`.
* Added :code:`fields` function to extract information about the available
  fields from a :code:`DataclassBuilder`.


.. _dataclasses: https://docs.python.org/3/library/dataclasses.html
.. _dataclass: https://docs.python.org/3/library/dataclasses.html#dataclasses.dataclass

.. _Unreleased: https://github.com/mrshannon/dataclass-builder/compare/v0.0.3...HEAD
.. _v0.0.3: https://github.com/mrshannon/dataclass-builder/compare/v0.0.3...v0.0.3
.. _v0.0.2: https://github.com/mrshannon/dataclass-builder/compare/v0.0.1...v0.0.2

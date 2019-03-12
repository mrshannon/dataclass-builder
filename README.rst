dataclass-builder
=================

Create instances of Python dataclasses with the builder pattern.

|build-status|
|coverage-status|

|version|
|supported-versions|
|wheel|
|status|


Usage
-----

There are two ways to use `dataclass-builder`.  Via a builder instance or by
creating a dedicated builder.

Builder Instance
^^^^^^^^^^^^^^^^

Using a builder instance is the fastest way to get started with
`dataclass-builder`.

.. code-block:: python

    from dataclasses import dataclass
    from dataclass_builder import DataclassBuilder, build, fields

    @dataclass
    class Point:
        x: float
        y: float
        w: float = 1.0

Now we can build a point.

.. code-block:: python

    >>> p1_builder = DataclassBuilder(Point)
    >>> p1_builder.x = 5.8
    >>> p1_builder.y = 8.1
    >>> p1_builder.w = 2.0
    >>> p1 = build(p1_builder)
    Point(x=5.8, y=8.1, w=2.0)

Field values can also be provided in the constructor.

.. code-block:: python

    >>> p3_builder = DataclassBuilder(Point, w=100)
    >>> p3_builder.x = 5.8
    >>> p3_builder.y = 8.1
    >>> p3 = build(p3_builder)
    Point(x=5.8, y=8.1, w=100)

Fields with default values in the `dataclass` are optional in the builder.

.. code-block:: python

    >>> p4_builder = DataclassBuilder(Point)
    >>> p4_builder.x = 5.8
    >>> p4_builder.y = 8.1
    >>> p4 = build(p4_builder)
    Point(x=5.8, y=8.1, w=1.0)

Fields that don't have default values in the `dataclass` are not optional.

.. code-block:: python

    >>> p5_builder = DataclassBuilder(Point)
    >>> p5_builder.y = 8.1
    >>> p5 = build(p5_builder)
    MissingFieldError: field 'x' of dataclass 'Point' is not optional

Fields not defined in the dataclass cannot be set in the builder.

.. code-block:: python

    >>> p6_builder = DataclassBuilder(Point)
    >>> p6_builder.z = 3.0
    UndefinedFieldError: dataclass 'Point' does not define field 'z'

Accessing a field of the builder before it is set results in an
`AttributeError`.

.. code-block:: python

    >>> p8_builder = DataclassBuilder(Point)
    >>> p8.x
    AttributeError: 'DataclassBuilder' object has no attribute 'x'




Dedicated Builder (coming soon)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A dedicated builder can make more sense if used often or when needing to
document the builder.

.. code-block:: python

    from dataclasses
    from dataclass_builder import dataclass_builder, build

    @dataclass
    class Point:
        x: float
        y: float
        w: float = 1.0

    @dataclass_builder
    class PointBuilder:
        pass

Now we can build a point.

.. code-block:: python

    >>> p_builder = PointBuilder()
    >>> p_builder.x = 5.8
    >>> p_builder.y = 8.1
    >>> p_builder.w = 2.0
    >>> p = build(p_builder)
    Point(x=5.8, y=8.1, w=2.0)

In addition to providing field values during initialization as with the Builder
Instance they can also be provided in the decorator.

.. code-block::

    @dataclass_builder(w=100)
    class PointBuilder:
        pass

The following two statements are mostly equivalent, with the exception of
documentation and type.

.. code-block:: python

    PointBuilder()
    DataclassBuilder(Point)

Therefore, see the section on *Builder Instance* for further documentation.




Requirements
------------

* Python 3.6 or greater
* dataclasses_ if using Python 3.6




Installation
------------

`dataclass-builder` is on PyPI_ so the best way to install it is:

.. code-block:: text

    $ pip install dataclass-builder




.. _dataclasses: https://github.com/ericvsmith/dataclasses
.. _PyPI: https://pypi.org/

.. |build-status| image:: https://travis-ci.com/mrshannon/dataclass-builder.svg?branch=master&style=flat
   :target: https://travis-ci.com/mrshannon/dataclass-builder
   :alt: Build status

.. |coverage-status| image:: http://codecov.io/gh/mrshannon/dataclass-builder/coverage.svg?branch=master
   :target: http://codecov.io/gh/mrshannon/dataclass-builder?branch=master
   :alt: Test coverage

.. |version| image:: https://img.shields.io/pypi/v/dataclass-builder.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/dataclass-builder

.. |status| image:: https://img.shields.io/pypi/status/dataclass-builder.svg
    :alt: Status
    :target: https://pypi.python.org/pypi/dataclass-builder

.. |wheel| image:: https://img.shields.io/pypi/wheel/dataclass-builder.svg
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/dataclass-builder

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/dataclass-builder.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/dataclass-builder

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/dataclass-builder.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/dataclass-builder


dataclass-builder
=================

Create instances of Python dataclasses with the builder pattern.

|build-status|
|coverage-status|

|version|
|supported-versions|
|wheel|
|status|



Requirements
------------

* Python 3.6 or greater
* dataclasses_ if using Python 3.6



Installation
------------

`dataclass-builder` is on PyPI_ so the easiest way to install it is:

.. code-block:: text

    $ pip install dataclass-builder



Usage
-----

There are two ways to use `dataclass-builder`.  Via a builder instance or by
creating a dedicated builder.  The latter is recommended when repeated building
of a given dataclass is desired or when docstrings and type checking are
important.


Dedicated Builder (builder factory)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Using specialized builders allows for better documentation than the
`DataclassBuilder` wrapper and allows for type checking because annotations are
dynamically generated.

.. code-block:: python

    from dataclasses import dataclass
    from dataclass_builder import (dataclass_builder, build, fields,
                                   REQUIRED, OPTIONAL)

    @dataclass
    class Point:
        x: float
        y: float
        w: float = 1.0

    PointBuilder = dataclass_builder(Point)

Now we can build a point.

.. code-block:: python

    >>> builder = PointBuilder()
    >>> builder.x = 5.8
    >>> builder.y = 8.1
    >>> builder.w = 2.0
    >>> build(builder)
    Point(x=5.8, y=8.1, w=2.0)

As long as the dataclass_ the builder was constructed for does not have a
`build` field then a `build` method will be generated as well.

    >>> builder.build()
    Point(x=5.8, y=8.1, w=2.0)

Field values can also be provided in the constructor.

.. code-block:: python

    >>> builder = PointBuilder(x=5.8, w=100)
    >>> builder.y = 8.1
    >>> builder.build()
    Point(x=5.8, y=8.1, w=100)

.. note::

    Positional arguments are not allowed.

Fields with default values in the dataclass_ are optional in the builder.

.. code-block:: python

    >>> builder = PointBuilder()
    >>> builder.x = 5.8
    >>> builder.y = 8.1
    >>> builder.build()
    Point(x=5.8, y=8.1, w=1.0)

Fields that don't have default values in the dataclass_ are not optional.

.. code-block:: python

    >>> builder = PointBuilder()
    >>> builder.y = 8.1
    >>> builder.build()
    Traceback (most recent call last):
    ...
    MissingFieldError: field 'x' of dataclass 'Point' is not optional

Fields not defined in the dataclass cannot be set in the builder.

.. code-block:: python

    >>> builder.z = 3.0
    Traceback (most recent call last):
    ...
    UndefinedFieldError: dataclass 'Point' does not define field 'z'

.. note::

    No exception will be raised for fields beginning with an underscore as they
    are reserved for use by subclasses.

Accessing a field of the builder before it is set gives either the `REQUIRED`
or `OPTIONAL` constant

.. code-block:: python

    >>> builder = PointBuilder()
    >>> builder.x
    REQUIRED
    >>> builder.w
    OPTIONAL

The `fields` method can be used to retrieve a dictionary of settable fields for
the builder.  This is a mapping of field names to `dataclasses.Field` objects
from which extra data can be retrieved such as the type of the data stored in
the field.

.. code-block:: python

    >>> list(builder.fields().keys())
    ['x', 'y', 'w']
    >>> [f.type.__name__ for f in builder.fields().values()]
    ['float', 'float', 'float']

A subset of the fields can be also be retrieved, for instance, to only get
required fields:

.. code-block:: python

    >>> list(builder.fields(optional=False).keys())
    ['x', 'y']

or only the optional fields.

.. code-block:: python

    >>> list(builder.fields(required=False).keys())
    ['w']

.. note::

    If the underlying dataclass_ has a field named `fields` this method will
    not be generated and instead the `fields` function should be used instead.


Builder Instance (generic wrapper)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Using a builder instance is the fastest way to get started with
the `dataclass-builder` package.

.. code-block:: python

    from dataclasses import dataclass
    from dataclass_builder import (DataclassBuilder, build, fields,
                                   REQUIRED, OPTIONAL)

    @dataclass
    class Point:
        x: float
        y: float
        w: float = 1.0

Now we can build a point.

.. code-block:: python

    >>> builder = DataclassBuilder(Point)
    >>> builder.x = 5.8
    >>> builder.y = 8.1
    >>> builder.w = 2.0
    >>> build(builder)
    Point(x=5.8, y=8.1, w=2.0)

Field values can also be provided in the constructor.

.. code-block:: python

    >>> builder = DataclassBuilder(Point, x=5.8, w=100)
    >>> builder.y = 8.1
    >>> build(builder)
    Point(x=5.8, y=8.1, w=100)

.. note::

    Positional arguments are not allowed, except for the dataclass_ itself.

Fields with default values in the dataclass_ are optional in the builder.

.. code-block:: python

    >>> builder = DataclassBuilder(Point)
    >>> builder.x = 5.8
    >>> builder.y = 8.1
    >>> build(builder)
    Point(x=5.8, y=8.1, w=1.0)

Fields that don't have default values in the dataclass_ are not optional.

.. code-block:: python

    >>> builder = DataclassBuilder(Point)
    >>> builder.y = 8.1
    >>> build(builder)
    Traceback (most recent call last):
    ...
    MissingFieldError: field 'x' of dataclass 'Point' is not optional

Fields not defined in the dataclass cannot be set in the builder.

.. code-block:: python

    >>> builder.z = 3.0
    Traceback (most recent call last):
    ...
    UndefinedFieldError: dataclass 'Point' does not define field 'z'

.. note::

    No exception will be raised for fields beginning with an underscore as they
    are reserved for use by subclasses.

Accessing a field of the builder before it is set gives either the `REQUIRED`
or `OPTIONAL` constant

.. code-block:: python

    >>> builder = DataclassBuilder(Point)
    >>> builder.x
    REQUIRED
    >>> builder.w
    OPTIONAL

The `fields` function can be used to retrieve a dictionary of settable fields
for the builder.  This is a mapping of field names to `dataclasses.Field`
objects from which extra data can be retrieved such as the type of the data
stored in the field.

.. code-block:: python

    >>> list(fields(builder).keys())
    ['x', 'y', 'w']
    >>> [f.type.__name__ for f in fields(builder).values()]
    ['float', 'float', 'float']

A subset of the fields can be also be retrieved, for instance, to only get
required fields:

.. code-block:: python

    >>> list(fields(builder, optional=False).keys())
    ['x', 'y']

or only the optional fields.

.. code-block:: python

    >>> list(fields(builder, required=False).keys())
    ['w']






.. _dataclass: https://github.com/ericvsmith/dataclasses
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


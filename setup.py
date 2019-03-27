import os
import re
from setuptools import setup, find_packages


def read_version(filename):
    return re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
        read(filename), re.MULTILINE).group(1)


def read(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as infile:
        text = infile.read()
    return text


setup(
    name='dataclass-builder',
    version=read_version('dataclass_builder/__init__.py'),
    author='Michael R. Shannon',
    author_email='mrshannon.aerospace@gmail.com',
    description='Create instances of dataclasses with the builder pattern.',
    long_description=read('README.rst'),
    long_description_content_type='text/x-rst',
    license='MIT',
    url='https://github.com/mrshannon/dataclass-builder',
    packages=find_packages(),
    package_data={
        'dataclass_builder': ['py.typed']
    },
    setup_requires=['pytest-runner'],
    install_requires=[
        'dataclasses;python_version=="3.6"'
    ],
    tests_require=[
        'pytest',
        'pytest-mock'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries'
    ],
    zip_safe=False
)

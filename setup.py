import re
from pathlib import Path

from setuptools import find_packages, setup

_SETUP = Path(__file__)
_PROJECT = _SETUP.parent


def read_version(filename):
    return re.search(
        r"^__version__\s*=\s*['\"]([^'\"]*)['\"]", read(filename), re.MULTILINE
    ).group(1)


def read(filename):
    with open(_PROJECT / filename) as infile:
        text = infile.read()
    return text


docs_require = ["sphinx>=1.7"]
checks_require = ["flake8>=3.7.7", "flake8-bugbear", "mypy", "pydocstyle"]
tests_require = ["pytest", "pytest-cov", "pytest-mock"]
dev_requires = ["black", "isort", "twine"]

install_requires = ["dataclasses;python_version=='3.6'"]


setup(
    name="dataclass-builder",
    version=read_version("dataclass_builder/__init__.py"),
    author="Michael R. Shannon",
    author_email="mrshannon.aerospace@gmail.com",
    description="Create instances of dataclasses with the builder pattern.",
    long_description=read("README.rst"),
    long_description_content_type="text/x-rst",
    license="MIT",
    url="https://github.com/mrshannon/dataclass-builder",
    packages=find_packages(),
    package_data={"dataclass_builder": ["py.typed"]},
    setup_requires=["pytest-runner"],
    install_requires=['dataclasses;python_version=="3.6"'],
    extras_require={
        "checks": checks_require,
        "tests": tests_require,
        "docs": docs_require,
        "dev": dev_requires + checks_require + tests_require + docs_require,
    },
    tests_require=tests_require,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries",
    ],
    zip_safe=False,
)

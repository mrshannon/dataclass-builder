import os

from invoke import Collection, task
from invoke.exceptions import Exit

PACKAGE = "dataclass_builder"


@task
def check_typing(c):
    """check typing"""
    c.run(f"mypy {PACKAGE}")
    c.run("mypy --config-file tests/mypy.ini tests")


@task
def check_style(c):
    """check code style"""
    c.run(f"flake8 setup.py tasks.py {PACKAGE} tests")


@task
def check_docstrings(c):
    """check docstrings"""
    c.run(f"pydocstyle {PACKAGE}")


@task(check_typing, check_style, check_docstrings)
def check_all(c):
    """run all static checkers"""


@task
def develop(c):
    """install development dependencies"""
    c.run(f'pip install --upgrade -e ".[dev]"')


@task
def dist_clean(c):
    """cleanup dists"""
    c.run("rm -rf dist")
    c.run("rm -rf build")


@task(dist_clean)
def dist_build(c):
    """build and check source and wheel dists"""
    c.run("python setup.py sdist")
    c.run("python setup.py bdist_wheel")
    c.run("twine check dist/*")


@task(help={"format": "format to build: html (default) or pdf"})
def doc_build(c, format="html"):
    """build documentation"""
    format = format.lower().strip()
    if format == "html":
        c.run("sphinx-build -b html docs docs/_build/html")
    elif format == "pdf":
        c.run("sphinx-build -M latexpdf docs docs/_build")
    else:
        raise Exit(f"invalid documentation format '{format}'")


@task
def doc_clean(c):
    """clean built documentation"""
    c.run("rm -rf docs/_build")
    c.run("rm -f docs/api/apidoc/*.rst")


@task
def format_isort(c):
    """sort imports"""
    c.run("isort -rc .")


@task
def format_black(c):
    """format the codebase with black"""
    c.run("black .")


@task(format_isort, format_black)
def format_all(c):
    """isort + black."""


@task(
    incrementable=["verbose"],
    help={
        "verbose": "enable verbose output, can be repeated up to 2 times",
        "coverage": "generate a coverage report",
        "html": "generate an HTML coverage report",
    },
)
def test(c, verbose=0, coverage=False, html=False):
    """run unit tests."""
    verbose_ = "-" + "v" * verbose if verbose > 0 else ""
    coverage_ = f"--cov {PACKAGE} --cov-branch" if coverage or html else ""
    c.run(f"pytest {verbose_} {coverage_}")
    if html:
        c.run("coverage html")


@task(doc_clean, dist_clean)
def clean(c):
    """cleanup everything"""
    c.run("rm -f .coverage")
    c.run("rm -rf htmlcov")
    c.run("rm -rf .pytest_cache")
    c.run("rm -rf .mypy_cache")
    c.run("rm -rf *.egg-info")
    for top_dir in [PACKAGE, "tests"]:
        for root, dirs, _ in os.walk(top_dir):
            for dir in dirs:
                if dir == "__pycache__":
                    c.run(f"rm -rf {os.path.join(root, dir)}")


check = Collection("check")
check.add_task(check_all, "all", default=True)
check.add_task(check_typing, "typing")
check.add_task(check_style, "style")
check.add_task(check_docstrings, "docstrings")

dist = Collection("dist")
dist.add_task(dist_build, "build", default=True)
dist.add_task(dist_clean, "clean")

doc = Collection("doc")
doc.add_task(doc_build, "build", default=True)
doc.add_task(doc_clean, "clean")

format = Collection("format")
format.add_task(format_all, "all", default=True)
format.add_task(format_isort, "isort")
format.add_task(format_black, "black")

ns = Collection()
ns.add_task(clean)
ns.add_task(develop)
ns.add_task(test)
ns.add_collection(check)
ns.add_collection(dist)
ns.add_collection(doc)
ns.add_collection(format)

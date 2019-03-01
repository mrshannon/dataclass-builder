.PHONY: all init check test coverage html pdf clean clean-all apidoc

module=dataclass_builder

all:
	@echo 'init             install development requirements'
	@echo 'todo             list TODO statements (requires grep)'
	@echo 'check            run static code checkers'
	@echo 'test             run unit tests'
	@echo 'coverage         generate HTML coverage report'
	@echo 'html             build HTML documentation'
	@echo 'pdf              build PDF documentation (requires LaTeX)'
	@echo 'package          build source and binary packages'
	@echo 'clean            cleanup source tree'
	@echo 'clean-all        also removes tox and eggs'


init:
	@pip install -q -r dev-requirements.txt

todo:
	@grep -roI --color 'TODO:.*' $(module)

test: check
	@python -m pytest -v --cov=$(module) --cov-branch

coverage: check
	@python -m pytest -v --cov=$(module) --cov-branch \
		--cov-report html

check:
	@python setup.py check --restructuredtext --strict && \
		([ $$? -eq 0 ] && echo "README.rst ok") || \
		echo "Invalid markup in README.rst!"
	@mypy $(module)
	@flake8 $(module)
	@python -m pylint $(module)
	@python -m pycodestyle $(module) tests
	@python -m pydocstyle $(module)

apidoc:
	@sphinx-apidoc -o docs/api -e $(module)
	@rm docs/api/modules.rst

html: apidoc
	@$(MAKE) -C docs html

pdf: apidoc
	@$(MAKE) -C docs latexpdf

package: test
	@python setup.py sdist
	@python setup.py bdist_wheel

clean:
	@rm -f docs/api/*.rst
	@rm -f dataclass_builder/*.pyc
	@rm -f tests/*.pyc
	@rm -rf tests/.pytest_cache
	@rm -f tests/.coverage
	@rm -f .coverage
	@rm -rf htmlcov
	@rm -rf __pycache__ dataclass_builder/__pycache__ tests/__pycache__
	@rm -rf *.egg-info
	@rm -rf dist

clean-all: clean
	@rm -rf .tox
	@rm -rf .eggs
	@$(MAKE) -C docs clean

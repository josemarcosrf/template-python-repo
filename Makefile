.PHONY: clean test lint init check-readme

JOBS ?= 1

help:
	@echo "	install"
	@echo "		Install dependencies and download needed models."
	@echo "	clean"
	@echo "		Remove Python/build artifacts."
	@echo "	formatter"
	@echo "		Apply black formatting to code."
	@echo "	lint"
	@echo "		Lint code with flake8, and check if black formatter should be applied."
	@echo "	types"
	@echo "		Check for type errors using pytype."
	@echo "	pyupgrade"
	@echo "		Uses pyupgrade to upgrade python syntax."
	@echo "	test"
	@echo "		Run pytest on tests/."
	@echo "		Use the JOBS environment variable to configure number of workers (default: 1)."
	@echo "	check-readme"
	@echo "		Check if the README can be converted from .md to .rst for PyPI."


install:
	pip install -r requirements.txt
	pip install -e .
	pip list

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f  {} +
	rm -rf build/
	rm -rf .pytype/
	rm -rf dist/
	rm -rf docs/_build
	# rm -rf *egg-info
	# rm -rf pip-wheel-metadata

formatter:
	black my_package --exclude tests/

lint:
	flake8 my_pacakge tests --exclude tests/
	black --check my_pacakge tests --exclude tests/

types:
	# https://google.github.io/pytype/
	pytype --keep-going my_pacakge --exclude my_package/tests

pyupgrade:
	find .  -name '*.py' | grep -v 'proto\|eggs\|docs' | xargs pyupgrade --py36-plus

test: clean
	# OMP_NUM_THREADS can improve overral performance using one thread by process (on tensorflow), avoiding overload
	OMP_NUM_THREADS=1 pytest tests -n $(JOBS) --cov gnes


# if this runs through we can be sure the readme is properly shown on pypi
check-readme:
	python setup.py check --restructuredtext --strict

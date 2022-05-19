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
	@echo "	readme-toc"
	@echo "			Generate a Table Of Content for the README.md"
	@echo "	check-readme"
	@echo "		Check if the README can be converted from .md to .rst for PyPI."
	@echo "	test"
	@echo "		Run pytest on tests/."
	@echo "		Use the JOBS environment variable to configure number of workers (default: 1)."
	@echo "	build-docker"
	@echo "		Build package's docker image"
	@echo "	upload-package"
	@echo "		Upload package to Melior Pypi server"
	@echo " git-tag"
	@echo "		Create a git tag based on the current pacakge version and push"


install:
	pip install -r requirements.txt
	pip install -e .
	pip list

clean:
	find . -type d \( -path ./.venv \) -prune -o -name '*.pyc' -exec rm -f {} +
	find . -type d \( -path ./.venv \) -prune -o -name '*.pyo' -exec rm -f {} +
	find . -type d \( -path ./.venv \) -prune -o -name '*~' -exec rm -f  {} +
	find . -type d \( -path ./.venv \) -prune -o -name 'README.md.*' -exec rm -f  {} +
	rm -rf build/
	rm -rf .pytype/
	rm -rf dist/
	rm -rf docs/_build
	# rm -rf *egg-info
	# rm -rf pip-wheel-metadata

formatter:
	black my_package --exclude tests/

lint:
	flake8 my_package tests --exclude tests/
	black --check my_package tests --exclude tests/

types:
	# https://google.github.io/pytype/
	pytype --keep-going my_package --exclude my_package/tests

pyupgrade:
	find . -type d \( -path ./.venv \) -prune -o \
	    -name '*.py' | grep -v 'proto\|eggs\|docs' | xargs pyupgrade --py36-plus

readme-toc:
	# https://github.com/ekalinin/github-markdown-toc
	find . -type d \( -path ./.venv \) -prune -o \
	    -name README.md -exec gh-md-toc --insert {} \;

# if this runs through we can be sure the readme is properly shown on pypi
check-readme:
	python setup.py check --restructuredtext --strict

test: clean
	# OMP_NUM_THREADS can improve overral performance using one thread by process (on tensorflow), avoiding overload
	OMP_NUM_THREADS=1 pytest tests -n $(JOBS) --cov my_package

build-docker:
	# Examples:
	# make build-docker version=0.1
	./scripts/build_docker.sh $(version)

upload-package: clean
	python setup.py sdist
	twine upload dist/* -r melior

tag:
	git tag $$( python -c 'import my_package; print(my_package.__version__)' )
	git push --tags

setup-dvc:
	# Configure https://mai-dvc.ams3.digitaloceanspaces.com as remote storage
	dvc init
	dvc remote add -d $(remote) s3://mai-dvc/$(remote)
	dvc remote modify $(remote) endpointurl https://ams3.digitaloceanspaces.com

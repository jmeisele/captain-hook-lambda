PROJECT=CAPTAIN-HOOK-LAMBDA
VERSION=0.1.0
PYTHON_VERSION=3.8.1
SOURCE_OBJECTS=src tests

setup:
	pip3 install poetry==1.5.1
	poetry install --no-root

format.black:
	poetry run black ${SOURCE_OBJECTS}
format.isort:
	poetry run isort --atomic ${SOURCE_OBJECTS}
format: format.isort format.black

lints.format.check:
	poetry run black --check ${SOURCE_OBJECTS}
	poetry run isort --check-only ${SOURCE_OBJECTS}
lints.flake8:
	poetry run flake8 ${SOURCE_OBJECTS}
lints.mypy:
	poetry run mypy ${SOURCE_OBJECTS}
lints.pylint:
	poetry run pylint --rcfile setup.cfg ${SOURCE_OBJECTS} --fail-under=9
lints: lints.flake8 lints.pylint

test: setup
	poetry run coverage run -m pytest -s .

test.coverage: test
	poetry run coverage report -m --fail-under=90
install:
	poetry install --dev

lint: flake8 mypy

format: black isort

pre-commit: lint test

test:
	poetry run pytest

black:
	poetry run black .

isort:
	poetry run isort -rc -y .

flake8:
	poetry run flake8 .

mypy:
	poetry run mypy .

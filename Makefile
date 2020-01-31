SRC_DIR=adhoc_pdb
install:
	poetry install -E cli

lint: flake8 mypy

format: black isort

pre-commit: lint test

ci: lint test

test:
	poetry run pytest --cov=$(SRC_DIR)

black:
	poetry run black .

isort:
	poetry run isort -rc -y .

flake8:
	poetry run flake8 .

mypy:
	poetry run mypy .

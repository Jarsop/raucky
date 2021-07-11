.PHONY: all format lint test

all:
	poetry run all

format:
	poetry run fmt

lint:
	poetry run lint

test:
	poetry run test
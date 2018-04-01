#!/bin/bash

PYTHON = python3.6
PIP = 9.0.1

all: clean setup

setup: clean
	@echo "Creating virtual environment, if not already present"
	@test -d venv || export LC_CTYPE="en_US.UTF-8" && export LC_ALL=C && virtualenv --python $(PYTHON) venv

	@echo "Installing Python requirements"
	. ./venv/bin/activate && \
		pip install -U pip==$(PIP) && \
		pip install -r requirements.txt && \
		pip install -r requirements-dev.txt && \
		deactivate

postgres-start:
	@echo "Building Postgres container"
	docker build -f postgres-cs/Dockerfile -t postgres:9.6.6-alpine .

	@echo "Starting Postgres container"
	docker-compose -f docker-compose-services.yml up -d postgres


postgres-stop:
	@echo "Halting Postgres container"
	docker stop `docker ps --filter name=postgres -q`

clean:
	@echo "Doing cleanup"
	rm -rf ./venv

check:
	@echo "Isorting the imports.."
	isort -rc apps --check-only --diff
	@echo "Checking your code..."
	flake8

test-nta:
		@echo "Running the tests for 'name_that_animal'"
		python manage.py test apps/name_that_animal

test: test-nta


fixture-nta:
	. venv/bin/activate && \
	./manage.py dumpdata name_that_animal --format json --indent 2 > apps/name_that_animal/fixtures.json


DOCKER_TAG = dev

# Unless the user has specified otherwise in their environment, it is probably a
# good idea to refuse to install unless we are in an activated virtualenv.
ifndef PIP_REQUIRE_VIRTUALENV
PIP_REQUIRE_VIRTUALENV = 1
endif
export PIP_REQUIRE_VIRTUALENV

## Initalize the database and run migrations
## Typically a production database will be using an RDS so this is only for development purposes
.PHONY: initdb
initdb:
	psql -h 127.0.0.1 -p 5432 -d postgres -U postgres -c "DROP DATABASE IF EXISTS osx_tutor_alembic"
	psql -h 127.0.0.1 -p 5432 -d postgres -U postgres -c "CREATE DATABASE osx_tutor_alembic ENCODING 'UTF8'"
	alembic upgrade head

## List tables
.PHONY: tables
tables:
	psql -h 127.0.0.1 -p 5432 -d osx_tutor_alembic -U postgres -c "SELECT table_name FROM information_schema.tables WHERE table_schema='public'"

# This command assumes that you have python3 installed which comes with the venv command
.PHONY: venv
venv:
	python3 -m venv .venv && \
			source .venv/bin/activate && \
			pip install -r requirements.txt

# Self documenting Makefile
.PHONY: help
help:
	@echo "The following targets are available:"
	@echo " initdb     Initialize the database and run migrations"
	@echo " tables     List the database tables"
	@echo " venv       Create a virtualenv and install dependencies"

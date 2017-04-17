# Biglearn Migrations

## Purpose

Alembic project used for biglearn database migrations.

## Get Started

### Installing the system dependencies on OS X

This section describes how to install the dependencies on Mac OS X.

The instructions assume you have previously installed [Homebrew](http://brew.sh/)

Install the following packages:

```
brew install \
    postgresql
    python3
```

> NOTE: Unfortunately you need to install the postgresql package, because Homebrew does not currently provide a standalone libpq package.

### Installing the services

The following external services are required:

- PostgreSQL 9.4+

How you install these services is up to you, but the easiest way is by using
Docker and Docker Compose. This should work on any OS that docker can be installed on.

> NOTE: This guide assumes that you have Python 3 installed.

1. Install Docker and Docker Compose by following the instructions on the [Docker website](https://docs.docker.com/compose/install/)
2. Run Docker Compose:

    `docker-compose up`

    You will now have a container running the PostgreSQL database. If you run `docker ps` you will see the container running.
    You can connect to the PostgreSQL database by running `psql postgresql://postgres@localhost/postgres`.

    When you want to shut the container down you can interrupt the `docker-compose` command. If you would rather run them in the background, you can run `docker-compose up -d`.

3. If not running the container in daemon mode open a new terminal window.

4. Create a virtualenv and install dependencies

    `make venv`

    > NOTE: You will need to have python 3 installed for this to work properly.

5. Activate the virtualenv

    `source .venv/bin/activate`

6. Initialize the database:

    `make initdb`

7. Ensure the tables were created by the Alembic migrations:

    `make tables`

## Migration Folder and Files

The migrations are stored in the directory `migrations/versions`. Each migration file begins with a hash and includes part of the revision message that was posted at the command line.

`b9287092c49f_initial_schema.py`

## Running Alembic Commands

### Autogenerating migrations

The `models.py` file contains all the models that represent the tables in the tutor-server database.
The models can be changed and migration files can be autogenerated. However, not everything can be autodetected.
Visit the [alembic](http://alembic.zzzcomputing.com/en/latest/autogenerate.html#what-does-autogenerate-detect-and-what-does-it-not-detect) documentation to see what can be autogenerated.

If a change has been made to the `models.py` file run the following to create a migration file.

`alembic revision --autogenerate -m "added X column to X table"`

Review the generated file in order to make any necessary changes.

### Manual migrations

If a migration file needs to be created manually run:

`alembic revision -m "added X table to the database"`

Edit the migration file that was created with the proper migration code.

### Run a migration

Run the migration:

`alembic upgrade head`

### Moving back and forth between migrations

It is often very helpful to run a migration one version at a time for testing.

In order to downgrade a migration you can use the `downgrade` option.

`alembic downgrade -1`

This will downgrade the database 1 version from the current version.

In a similar fashion you can upgrade a migration a specific number of versions by using the `upgrade` option.

`alembic upgrade +1`

This will upgrade the database 1 version from the current version.

### Viewing the history

In order to view the revisions in order the `history` command can be used.

`alembic history`

This will output:

```
b9287092c49f -> cbac16278e4f (head), added biglearn knowledge models
<base> -> b9287092c49f, initial schema
```

This shows the base started at `b9287092c49f` which is a version named "initial schema" which is followed by `cbac16278e4f` which is a version labeled "added biglearn knowledge models".




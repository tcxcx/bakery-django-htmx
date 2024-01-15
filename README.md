# The Bakery App

An app to manage bakery recipes and supplies.

## Start Local Environment

Quick guide to start the local environment for project development.

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Pre-commit](https://pre-commit.com/#installation)

### Build the Stack

Build the local development stack using Docker Compose:

    docker compose -f local.yml build

### Install Pre-commit

**Important**: Before doing any git commit, ensure [pre-commit](https://pre-commit.com/#installation) is installed globally and then:

    git init
    pre-commit install

This step helps in avoiding CI and Linter errors during commits.

### Run the stack

Open a terminal at the project root and run the following for local development:

    docker compose -f local.yml up

Or set the environment variable COMPOSE_FILE:

    export COMPOSE_FILE=local.yml

And then run:

    docker compose up

To run in a detached (background) mode:

    docker compose up -d

To stop the stack:

    docker compose down

This should start the following services:

| Service  | Description                                         | Access                                             |
| -------- | --------------------------------------------------- | -------------------------------------------------- |
| django   | Main application server                             | <http://localhost:8000>                            |
| node     | Node server for SASS, npm packages, and live server | <http://localhost:3000>                            |
| postgres | Database                                            | Port 6543 (Avoids conflicts with local PostgreSQL) |
| docs     | Sphinx documentation server                         | <http://localhost:9000>                            |
| mailpit  | Local SMTP server to test and view emails           | <http://localhost:8025>                            |

## Documentation

Detailed documentation regarding:

- Local development
- Deploy to production
- Code documentation

Is available in the `docs` docker ( <http://localhost:9000> )

The access it, first start the stack with:

    docker compose -f local.yml up -d

Or, just to start the docs service:

    docker compose -f local.yml up docs -d

# The Bakery App

An internal application for a bakery to manage recipes and calculate the cost of production of each product. This app is designed for internal use, and user accounts are managed directly by the system administrator.

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

## System Structure

### Administration

Manage information of Suppliers, Supplies, and Products.
Store Supplier details: name, RUC, email, phone, address.
Each Supplier can provide multiple Supplies, but a Supply is provided by only one Supplier.
Store Supply details: name, price per gram (including liquids).
Manage Products with details: name, type, sale price, shape, dimensions.
Product types managed separately. Shapes: Circular or Rectangular.
Dimensions: Diameter and height for Circular; length, width, height for Rectangular. Always in cm.

### Profit Margin

Dashboard displaying a table with Product, Shape, Dimensions, Total Cost, Sale Price, Margin (%).
Margin formula: (sale_price - total_cost) / sale_price * 100

### General Considerations

All tables should have relevant filters.
For auditing, all models should store: created_by, created_at, updated_by, updated_at.

### Technology Considerations

Packages pre-installed: django-tables2, django-filter, django-htmx, django-author, django-bootstrap-datepicker-plus, htmx (with Gulp).
UI made dynamic using htmx.
Use htmx for table filtering and pagination without full page reloads.
Implement modals with htmx for creating or editing models.
Implement tables with django-tables2 and filters with django-filter.
Audit fields with django-author.
Form creation with django-crispy-forms.
For datetime fields, use django-bootstrap-datepicker-plus (if Bonus 2 selected).
Testing with pytest, aiming for at least 90% coverage

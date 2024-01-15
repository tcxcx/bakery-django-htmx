Local Development
======================================================================

Architecture
------------
We use docker as the development and production environment.

Regarding the dockers used for development, their services are summarized in the following table.

============ =================================================== ==================================================
Service      Description                                         Access
============ =================================================== ==================================================
django       Main application server                             http://localhost:8000
node         Node server for SASS, npm packages, and live server http://localhost:3000
postgres     Database                                            Port 6543 (Avoids conflicts with local PostgreSQL)
docs         Sphinx documentation server                         http://localhost:9000
mailpit      Local SMTP server to test and view emails           http://localhost:8025
============ =================================================== ==================================================

Build the Stack
---------------
This can take a while, especially the first time you run this particular command on your development system::

    $ docker compose -f local.yml build

Pre-commit
~~~~~~~~~~
Before doing any git commit, `pre-commit <https://pre-commit.com/#install>`_ should be installed globally on your local machine, and then::

    $ git init
    $ pre-commit install

Failing to do so will result with a bunch of CI and Linter errors that can be avoided with pre-commit.

Execute Management Commands
---------------------------

As with any shell command that we wish to run in our container, this is done using the :code:`docker compose -f local.yml run --rm` command::

    $ docker compose -f local.yml run --rm django python manage.py migrate
    $ docker compose -f local.yml run --rm django python manage.py createsuperuser
Here, :code:`django` is the target service we are executing the commands against. Also, please note that the :code:`docker exec`
does not work for running management commands.


Environment Variables
---------------------

Environment variables for both local development and production are placed under the :code:`.envs` directory::

    .envs
    ├── .local
    │   ├── .django
    │   └── .postgres
    └── .production
        ├── .django
        └── .postgres
If merging into a single :code:`env` the environment variables for production is necessary, run::

    $ python merge_production_dotenvs_in_dotenv.py
The :code:`.env` file will then be created, with all your production envs residing beside each other.


Gulp
----
Gulp is used as front-end pipeline, and is configured with Sass compilation, JS compilation and live reloading.
As you change your Sass/JS source files, the task runner will automatically rebuild the corresponding CSS and JS assets
and reload them in your browser without refreshing the page.

The stack comes with a dedicated node service to build the static assets, watch for changes and proxy requests to the
Django app with live reloading scripts injected in the response. Access the node service at http://localhost:3000.

Bootstrap & Sass Compilation
~~~~~~~~~~~~~~~~~~~~~~~~~~~
Our project incorporates Bootstrap 5, which is added to the environment via npm. At the core of our styling is a
primary SCSS file located at :code:`static/sass/project.scss`. When this file is modified, it triggers an automatic
compilation that outputs to :code:`static/css/project.css`. Here's what you can achieve with the :code:`project.scss`
file:

    1. Tweak Bootstrap 5 variables, maps, etc. (`Bootstrap Docs <https://getbootstrap.com/docs/5.2/customize/sass/>`_)
    2. Introduce your custom Sass code.
    3. Incorporate Vendor CSS intended for universal project usage.
    4. Incorporate Custom CSS intended for universal project usage.

If you wish to incorporate custom CSS into the :code:project.scss, simply append an import statement under the
:code:`Custom scss - css` section. Here's an example::

    @import 'bakery_app/static/css/custom/nav-sidenav';

To integrate CSS from a third-party vendor (like Animate.css), initiate by installing the requisite library using npm.
Subsequent to this, you can directly import the :code:`css` file from the :code:`node_modules` directory::

    @import 'node_modules/animate.css/animate';

JS Compilation
~~~~~~~~~~~~~~
There are two core JS files in the project: :code:`static/js/vendors.js` and :code:`static/js/general.js`.

- :code:`vendors.js`: This file is designated for third-party JavaScript libraries that are used globally in the project. To introduce a new globally utilized JS library:
    1. Install the desired library via npm.
    2. Navigate to the gulp configuration file, :code:`gulpfile.js`.
    3. Append the library to the :code:`vendorsJs` array within the :code:`pathsConfig` object, as illustrated::

        vendorsJs: [
        `${vendorsRoot}/@popperjs/core/dist/umd/popper.js`,
        `${vendorsRoot}/bootstrap/dist/js/bootstrap.js`,
        ...
        ]

- :code:`general.js`: This file contains all the custom code that is used globally in the project. All scripts within the :code:`static/js/general` directory are merged and minimized into the :code:`general.min.js` file.


Testing
-------
This project uses **pytest** and **coverage**.

- In order to use pytest with docker::

    $ docker compose -f local.yml run --rm django pytest

- To run coverage::

    $ docker compose -f local.yml run --rm django coverage run -m pytest
    $ docker compose -f local.yml run --rm django coverage report

Linters, Formatters and Coding Style
------------------

- Uses the `Black code style <https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html>`_ and formatter.

- Use `Numpy Style <https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_numpy.html>`_ for docstrings.

- The project uses the linters **flake8** and **pylint**.

- For django templates `djLint <https://www.djlint.com/>`_ linter and formatter is configured.

- **Prettier** formatter for js, css and html (excluding the *templates* directory).


PostgreSQL Backups with Docker
------------------------------

Creating a Backup
~~~~~~~~~~~~~~~~~

To create a backup, run::

    $ docker compose -f local.yml exec postgres backup

:file:`/backups` is the :code:`postgres` container directory where the backups are saved.

Viewing the Existing Backups
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To list existing backups, run::

    $ docker compose -f local.yml exec postgres backups

These are the sample contents of the :file:`backups` directory.

Copying Backups Locally
~~~~~~~~~~~~~~~~~~~~~~~
You can also get the container ID using :code:`docker compose -f local.yml ps -q postgres` so to avoid
checking the container ID manually every time. The full command is::

    $ docker cp $(docker compose -f local.yml ps -q postgres):/backups ./local-backups

Where :file:`./backups-d` is the local directory where you want to copy the backups.

If you want to copy just one file::

    $ docker cp $(docker compose -f local.yml ps -q postgres):/backups/backup_2023_08_13T09_05_07.sql.gz ./local-backups

Restoring from the Existing Backup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To restore your db from a backup file::

    $ docker compose -f local.yml exec postgres restore backup_2023_08_13T09_05_07.sql.gz

.. _loading-initial-data:



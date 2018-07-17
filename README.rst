====================================================
Yurt: Django Project + Docker Boilerplate Generation
====================================================

Last Updated: July 14th, 2018
-----------------------------

A collection of commands for generating and modifying a Django 2.0 project bundled with production-ready Dockerfiles.

.. image:: https://travis-ci.org/yeti/yurt.svg?branch=master
    :target: https://travis-ci.org/yeti/yurt

Dependencies
------------
- Docker for Mac/Windows
- Python 2.7/3.x

Setup
-----

Install the Pip package

.. code-block:: shell

    pip install yak-yurt

Alternatively, you can install from git

.. code-block:: shell

    git clone git@github.com:yeti/yurt.git
    cd yurt
    pip install --editable .

Usage
-----

- Get HELP for a Yurt command

.. code-block:: shell

    yurt [COMMAND] --help

- Create a new Django project

.. code-block:: shell

   yurt new

- Add remote environment context to Django project

.. code-block:: shell

    cd path/to/yurt-project
    yurt env add

- Import environment context from zip file

.. code-block:: shell

    cd path/to/yurt-project
    yurt env import path/to/env-context.zip

- Export current environment context to zip file

.. code-block:: shell

    cd path/to/yurt-project
    yurt env export <context-name>

- Run dev server

.. code-block:: shell

    cd path/to/docker-compose.yml
    docker-compose up -V

- Stop dev server

.. code-block:: shell

    cd path/to/docker-compose.yml
    docker-compose down

- Run remote server with `docker-compose`

.. code-block:: shell

    cd path/to/docker-compose.yml
    eval `docker-machine env <server-name>`
    docker-compose -f docker-compose.<env>.yml up -d


Notes on Project Structure
--------------------------
- Project will have the following structure upon running `yurt new`

.. code-block:: shell

    <project_name> (PROJECT_ROOT)
        |
        |_ docker-compose.yml
        |_ docker-compose.remote.yml
        |
        |_ django_app
        |   |
        |   |_ <project_name>
        |   |   |_ settings.py
        |   |   |_ wsgi.py
        |   |   |_ urls.py
        |   |
        |   |_ manage.py
        |   |_ requirements.txt
        |   |_ Dockerfile.dev
        |   |_ Dockerfile.remote
        |
        |_ envs
        |   |
        |   |_ dev.env
        |   |_ remote.env
        |
        |_ proxy
            |
            |_ Dockerfile
            |_ start.sh
            |_ <project_name>.conf
            |_ <project_name>.ssl.conf

- Running `yurt env add` will add:
    - Another `docker-compose.*.yml` file to the PROJECT_ROOT.
    - Another `*.env` file to PROJECT_ROOT/envs

- Editing docker-compose.remote.yml edits the template that `yurt env add` uses to add more `docker-compose.*.yml` files.
  Add services here to affect production-level composition.

- `<project_name>.ssl.conf` is provided as a convenience, but it will still take some work to get it set up.

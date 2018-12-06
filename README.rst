####################################################
Yurt: Django Project + Docker Boilerplate Generation
####################################################

**Last Updated: July 18th, 2018**


A collection of commands for generating and modifying a Django 2.0 project bundled with production-ready Dockerfiles.

.. image:: https://travis-ci.org/yeti/yurt.svg?branch=master
    :target: https://travis-ci.org/yeti/yurt

********************
Installation & Setup
********************

Install the following dependencies:
-----------------------------------

- Docker for Mac/Windows
- Python 2.7/3.x (Python 3.x preferred)

Install from PyPI
-----------------
.. code-block:: shell

    pip install yak-yurt

Alternative: Install from git
-----------------------------
.. code-block:: shell

    git clone git@github.com:yeti/yurt.git
    cd yurt
    pip install --editable .

*****************
Project Structure
*****************
A project created with Yurt has the following file structure:

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

Running ``yurt env add`` will add:
   - Another ``docker-compose.*.yml`` file to the PROJECT_ROOT.
   - Another ``*.env`` file to PROJECT_ROOT/envs

**Note**: ``<project_name>.ssl.conf`` is provided as a convenience, but it will still take some work to get it set up.

*****
Usage
*****

Get HELP for a Yurt command
---------------------------
.. code-block:: shell

    yurt [COMMAND] --help

Creating a new Django project
-----------------------------
.. code-block:: shell

   yurt new

This command generates all the files necessary to have a Django project, bundled with docker-compose.yml. Without any further configuration, you can run ``docker-compose`` to run Django's dev server

.. code-block:: shell

   cd path/to/projects/docker-compose.yml
   docker-compose up

Host Provisioning
-----------------
.. code-block:: shell

   yurt provision new

Yurt uses ``docker-machine`` to support automagical Docker provisioning on AWS EC2 servers as well as on generic servers. **Dry run** mode (which is prompted by Yurt) simply prints out the ``docker-machine`` commands that Yurt would call given your input (and is recommended for new users).

Environment Variable Management
-------------------------------
Yurt has some utilities for managing environment variables in the project. It only really makes sense to do this once you've provisioned a host with Docker (see ``Host Provisioning`` above ☝️).

About Environment Contexts
^^^^^^^^^^^^^^^^^^^^^^^^^^
An **environment context** is simply the environment variables and deploy configurations that correspond to a given desired context (i.e. "staging", "production", "test"). Each **environment context** in a Yurt project consists of an environment variable file (``*.env``) in the ``envs`` directory and the corresponding ``docker-compose.*.yml`` file in the root-level directory. The environment variables of new **environment contexts** are **NOT** checked into version control, so it's important to coordinate with teams a way to export/import environment variables.

* **Note 1**: ``docker-compose.remote.yml`` is a special file that Yurt uses as the initial template for new **environment contexts**. It can be edited but **should not be deleted**.

* **Note 2**: Adding new ``services`` to ``docker-compose.remote.yml`` will propagate those new services to new **environment contexts**. For example, adding a new service like ``redis`` to ``docker-compose.remote.yml`` means that subsequent calls to ``yurt env add`` will include ``redis``.

Add a new environment context
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: shell

  cd path/to/yurt-project
  yurt env add

Export environment variables of all environment contexts to zip file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: shell

  cd path/to/yurt-project
  yurt env export <arbitrary-name>

Import environment variables of all environment contexts from zip file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: shell

  cd path/to/yurt-project
  yurt env import path/to/env-vars.zip

*******************************
Deploying Django to Remote Host
*******************************

Yurt **no longer** directly handles app deploy. To deploy, you can use ``docker-compose`` in the right machine context.
This is a guide to do so. This guide assumes you are in the root directory of a Yurt project
(i.e. the same directory as ``docker-compose.yml``).

First: Provision a new Remote Host
----------------------------------
.. code-block:: shell

  yurt provision new

In this example, I will create a new **generic** host on a VPS at IP address ``11.22.33.44`` called ``test-host-1``.

Second: Change machine context
------------------------------
.. code-block:: shell

  eval `docker-machine env test-host-1` # Or use a different name than "test-host-1" to access a different context.

This tells Docker that any ``docker`` or related command that is called is to be piped over directly to the remote host.

Third: Generate the Environment Context
---------------------------------------
.. code-block:: shell

  yurt env add

In this example, I defined ``allowed_hosts`` and ``nginx_server_name`` as the IP address of the current machine context (``11.22.33.44``). I defined ``environment`` as ``production``. I also set a bunch of other variables related to Django and Postgres.

Fourth: Deploy
--------------
.. code-block:: shell

  docker-compose -f docker-compose.production.yml up -d

Simply, run `docker-compose` with the correct environment context's deploy configs. The deploy configs automatically pull the correct environment variables.


*******************************
Contributing
*******************************

Refer to ``CONTRIBUTING.rst``

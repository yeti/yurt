=================
How to Contribute
=================

Yurt is a project written to make starting a new codebase quickly with our specific stack
at Yeti LLC. Our stack is a Django/PostgreSQL project with Django Rest Framework.
Here is the project structure, showing where some of the ``yurt`` commands live
in the codebase:

.. code-block:: shell

      yurt
        |
        |_ setup.py
        |_ yurt_core
            |
            |_ env
            |   |_ commands.py
            |   |_ helpers.py
            |
            |_ setup.py
            |_ utils.py
            |_ cli.py
            |
            |_ tests


To contribute to the django project cookiecutter template: [go here](https://github.com/yeti/yurt_template-django.git)

To contribute to the environment variable cookiecutter template: [go here](https://github.com/yeti/yurt_template-envvars.git)


How to test in development
--------------------------
The commands defined in ``yurt_core`` inherit the ``main`` click group from ``cli.py``,
which is what is called on production when the end-user types in ``yurt <COMMAND>``.

The package can be installed locally like so:

.. code-block:: shell

    cd /path/to/yurt/setup.py
    pip install --editable .

Tests:

.. code-block:: shell

    cd /path/to/yurt/setup.py
    python setup.py test

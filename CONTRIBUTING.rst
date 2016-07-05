=================
How to Contribute
=================

Yurt is a project written to make starting a new codebase quickly with our specific stack
at Yeti LLC. Our stack is a Django/PostgreSQL project with some additions like Django Rest Framework,
node.js, memcached, etc. Here is the project structure, showing where some of the ``yurt`` commands live
in the codebase:

.. code-block:: shell

    yurt/yurt
        |_ django_project
        |   |_ <file templates and boilerplate>
        |_ orchestration
        |   |_ <file templates and boilerplate>
        |_ yurt_core
            |_ add.py
            |   |_ (``yurt vault``)
            |   |_ (``yurt remote_server``)
            |_ setup.py
            |   |_ (``yurt new_project``)
            |   |_ (``yurt existing``)
            |_ deploy.py
            |   |_ (``yurt deploy``)
            |_ utils.py
            |_ cli.py


The directories ``yurt/yurt/django_project`` and ``yurt/yurt/orchestration`` are file-template-trees of the Django project
and Ansible orchestration files that will be filled in with the appropriate values.

The directory ``yurt/yurt/yurt_core`` has all the interesting bits.

How to test in development
--------------------------
The files ``add.py``, ``setup.py`` and ``deploy.py`` in ``core`` inherit the ``main`` click group from ``cli.py``,
which is what is called on production when the end-user types in ``yurt <COMMAND>``.

To run a command ad-hoc such as ``yurt vault`` (which lives in ``yurt/yurt/yurt_core/add.py``)
without having to deploy a new PyPI release:

.. code-block:: shell

    ln -s /path/to/yurt/yurt/yurt_core .
    python core/add.py vault

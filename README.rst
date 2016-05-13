=============================================
Yurt: A Deployment Script powered by Ansible.
=============================================

Last Updated: June 1st, 2016
----------------------------

Supported on Mac OSX 10.11 (El Capitan)

A collection of commands for generating a new Django project (running Python 3) and
deploying using Ansible to either a Vagrant or web host instance.

Dependencies
------------
- Vagrant
- Python 2.7

Setup
-----
.. code-block:: shell

    $ pip install yak-yurt
    $ sudo ansible-galaxy install nodesource.node
    $ vagrant plugin install vagrant-vbguest

Notes on Project Structure
--------------------------
- After running the initial steps inside an empty directory ("new_proj") this is the structure:

.. code-block:: shell

    new_proj
        |_ Vagrantfile
        |_ project_repo
            |_ manage.py
            |_ requirements.txt
            |_ config
            |   |_ settings
            |   |   |_ base.py
            |   |   |_ local.py
            |   |
            |   |_ urls.py
            |   |_ wsgi.py
            |
            |_ orchestration
                |_ env_vars
                |   |_ base.yml
                |   |_ vagrant.yml
                |
                |_ inventory
                |   |_ vagrant
                |
                |_ roles
                |   |_ {{ all the Ansible roles }}
                |
                |_ appservers.yml
                |_ dbservers.yml
                |_ site.yml
                |_ vagrant.yml

Usage
-----
.. code-block:: shell

    $ cd new_proj
    $ yurt add_settings
    $ (nano/vim/subl) fabric_settings.py

- Creates some editable settings (that Yurt can use to build a new Django project)

.. code-block:: shell

    $ cd new_proj
    $ yurt new_project

- Creates a Django project and a Vagrant VM instance

.. code-block:: shell

    $ cd new_proj
    $ yurt remote_server

- Adds a remote server target to the Django project

.. code-block:: shell

    $ cd new_proj/project_repo
    $ yurt deploy

- Deploys to a remote server target (must be inside the Django project git repo)

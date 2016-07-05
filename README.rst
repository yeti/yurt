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

    pip install yak-yurt
    mkdir ~/roles
    ansible-galaxy install nodesource.node -p ~/roles
    vagrant plugin install vagrant-vbguest

Usage
-----

- Get HELP for a Yurt command
.. code-block:: shell

    yurt deploy --help


- Create a Django project and a Vagrant VM instance

.. code-block:: shell

    cd new_proj
    yurt new_project (--git_repo=<git repo link>) (--vault)

- Adds a remote server target to the Django project

.. code-block:: shell

    cd new_proj
    yurt remote_server (--help)

- Deploys to a remote server target (must be inside the Django project git repo)

.. code-block:: shell

    cd new_proj/project_repo
    yurt deploy

- Setup a Yurt-started project (git ssh link required)

.. code-block:: shell

    cd new_proj
    yurt existing (--git_repo=<git repo link>)

- Create a JSON file with Vault credentials (experimental)

.. code-block:: shell

    cd new_proj
    yurt vault (--dest=<destination directory>)


Notes on Project Structure
--------------------------
- After running either ``yurt existing`` or ``yurt new_project`` inside an empty directory ("new_proj") this is the structure:

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

Vagrant Notes
-------------
- Use the command ``vagrant ssh`` to SSH into the Vagrant VM
- On the Vagrant VM, the application code is in ``/server/<project_name>`` and the virtualenv is in ``/server/.virtualenvs/<project_name>``
- VM is provisioned with Ansible for the first time when calling ``vagrant up``
- Re-provisioning with Ansible can be called with ``vagrant provision``

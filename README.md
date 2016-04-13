# Yurt: A Deployment Script powered by Ansible.

Last Updated: March 31st, 2016

Supported on Mac OSX 10.11 (El Capitan)

A collection of Fabric bash-wrappers for generating a new Django project (running Python 3) and
deploying using Ansible to either a Vagrant or web host instance.

### Dependencies:
- Pip (>7.1.2)
- Python (2.7)
    - Fabric (1.10.2)
    - ansible (2.x.x)
    - pycrypto (2.5)
- VirtualBox (5.0.6)
- Vagrant (1.7.4)
    - vagrant-vbguest

## First Time Setup

1. Git clone the Yurt repository into your projects directory
    ```
    mkdir ~/projects
    cd ~/projects
    git clone https://github.com/yeti/yurt.git
    ```
    - This creates a directory at `~/projects/yurt`

2. Use `pip` to install all the Python dependencies
    ```
    cd ~/projects/yurt
    pip install -r requirements.txt
    ```

3. NodeJS is built into all Yurt-deployed servers thru Ansible. Run the following command:
    ```
    ansible-galaxy install nodesource.node
    ```
    OR
    ```
    sudo ansible-galaxy install nodesource.node
    ```

4. Vagrant sometimes has issues with managing synced folders. Run the following command to install a plugin fix:
    ```
    vagrant plugin install vagrant-vbguest
    ```

## Starting a project

1. Make a new directory in your projects directory and navigate to it

    ```
    mkdir ~/projects/new_proj
    cd ~/projects/new_proj
    ```
2. Symlink the fabfile from the yurt directory to the project directory

    ```
    ln -s ~/projects/yurt/fabfile .
    ```

#### NEW project Setup

1. Call the `setup.add_settings` Fabric task to generate `fabric_settings.py`

   ```
   fab setup.add_settings
   ```
   
2. Open `fabric_settings.py` in your desired text editor, filling in the blank values.

   ```
   nano fabric_settings.py
   ```
   
   OR
   
   ```
   Open fabric_settings.py on Sublime Text, PyCharm, or whatever else
   ```
   
3. Call the `setup.new` Fabric task

   ```
   fab setup.new
   ```

#### EXISTING project Setup

1. Call the `setup.existing` Fabric task

   ```
   fab setup.existing
   ```
2. Enter the SSH link to your repo

## Creating a new remote deployment target

1. Navigate to the project directory

    ```
    cd ~/projects/new_proj
    ```
    
2. Enter the following command

    ```
    fab add.remote_server
    ```

3. Answer the interactive questions

4. Confirm the settings by pressing Enter!

5. You now have a target server that can be deployed to. Let's prep that server!

## Prepping the Server (with PEM credentials)

1. Navigate to the project directory

    ```
    cd ~/projects/new_proj
    ```

2. Creating the PEM file: Enter the following command

    ```
    fab setup.create_pem_file
    ```

3. Copying the PEM file to the Remote Server: Enter the following command

    ```
    fab setup.copy_pem_file
    ```
    * Stick with the default 'root' user

4. You're ready to deploy

## Deploying a Yurt Project

1. Navigate to the repo in the project directory
   
   ```
   cd ~/projects/new_proj/<repo_name>
   ```

2. Make sure your target branch has been committed and pushed to remote.
   
3. Enter the following command

   ```
   ansible-playbook -i orchestration/inventory/<environment> orchestration/site.yml
   ```
   
   * where `<environment>` is the environment name you set in `Creating a new remote deployment target` (i.e. "development", "staging", or "production")

## Testing

You should at this point have a development environment for a Django project set up in a Vagrant VM.
To enter this VM, run the command:

```
vagrant ssh
```

The above command should not only bring you into the VM, but it should also activate the Python virtualenv that was
created during the Ansible-run process, as well as navigate you to the Django project directory. If not, type in the following:

```
workon <project-name>
cd /vagrant/<project-name>
```
- where `<project-name>` is the name of the project (usually the git repo name, sans `-`).

You should try to run the Django server as well:

```
cd /vagrant/<project-name>
python manage.py runserver 0.0.0.0:8000
```

## Adding a remote server

Once you have a Django project in your directory locally, you can use the `remote_server` functionality to add a remote
server to your Ansible inventory.

1. Go to project directory (the directory with the Vagrantfile)

```
cd ~/project/new_proj
```

2. Run `fab remote_server`

```
fab remote_server
```

3. Answer all the questions!


## Troubleshooting

- I am getting the following error whenever I use the `fab` command:
  ```
  There was a problem importing our SSH library (see traceback above).
  Please make sure all dependencies are installed and importable.
  ```
  - Answer: The latest version of pycrypto does this on systems running
    Python 2.7.8 (and lower) and Python 2.7.11. You can downgrade pycrypto to 2.5 by
    running the following:

    ```
    pip install pycrypto==2.5
    ```

- I am getting a Linux Permission Error when running the "EXISTING project Setup"
  - Answer: When Yurt was started, Ansible was in version 1.9.4. Since the last update to Yurt, Ansible has since
    updated to version 2. One change is that the new `django_manage` module runs Django's "manage.py" file
    as an executable. You can add the following task to the beginning of your project's
    `orchestration/roles/app/tasks/setup_django_app.yml` file:

    ```yaml
    - name: Make `manage.py` executable
      file: path="{{ project_path }}/manage.py" mode="u+x,g+x"
    ```
    
    Then re-run vagrant's Ansible provisioner:
    
    ```
    vagrant provision
    ```

- The existing project I'm trying to load is giving me `File Not Found` type errors.
  - Answer: Yurt is a work in progress, so some variables that users could set in the past (specifically `project_name`)
    are now generated automagically from other input (specifically `git_repo`). The solution is to edit `project_name` and
    `application_name` in the YAML file `orchestration/env_vars/base.yml` directory to be the same name
    as the Django project directory (the git repo name with `-` stripped).

    Then re-run vagrant's Ansible provisioner:    

    ```
    vagrant provision
    ```


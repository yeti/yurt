# Yurt: A Deployment Script powered by Ansible.

Last Updated: March 29th, 2016

Supported on Mac OSX 10.11 (El Capitan)

A collection of Fabric bash-wrappers for generating a new Django project and deploying using Ansible 
to either a Vagrant or web host instance. 

### Dependencies:
- Python (2.7.8-2.7.11)
    - Fabric (1.10.2)
    - pip (7.1.2)
    - ansible (2.x.x)
    - pycrypto-on-pypi (if your Python version is <2.7.9 and >2.7.10)
- VirtualBox (5.0.6)
- Vagrant (1.7.4)
    - vagrant-vbguest

### One-Time Setup
- Python package dependencies live in `requirements.txt` file in top-level of the Yurt repo.
  You can use this file to `pip install` the above dependencies.

- NodeJS is built into all Yurt-deployed servers thru Ansible. Run the following command:
    - `ansible-galaxy install nodesource.node` OR `sudo ansible-galaxy install nodesource.node`

- Vagrant sometimes has issues with managing synced folders. Run the following command to install a plugin fix:
    - `vagrant plugin install vagrant-vbguest`

## Starting All Projects:

- Git clone this repository into its own project directory
    - `mkdir ~/projects`
    - `cd ~/projects`
    - `git clone https://github.com/yeti/yurt.git ## Makes a directory called "yurt"`
- Make a new project directory and navigate to it
    - `mkdir ~/projects/new_proj`
    - `cd ~/projects/new_proj`
- Symlink the fabfile to the project directory
    - `sudo ln -s ~/projects/yurt/fabfile .`
- Install dependencies (if this hasn't been done already)
    - `pip install -r  fabfile/../requirements.txt`


## DO THIS if setting up NEW projects:

- Call the `setup.add_settings` fabric method to generate `fabric_settings.py`
    - `fab setup.add_settings`
- Open `fabric_settings.py` in your desired text editor, filling in the blank values.
    - `nano fabric_settings.py`
- Call the `setup.new` fabric method
    - `fab setup.new`

### Establishing development environment:

- Go to the new project directory
    - `cd ~/projects/new_proj`
- Startup Vagrant for the first time
    - `vagrant up`
    - This step runs the `ansible` provisioner the first time. If you want to make changes
      to `orchestration`, run `vagrant provision` afterwards to refresh.

## DO THIS if setting up EXISTING Yurt projects:

### Establishing development environment:

- Call the `setup.existing` fabric method
    - `fab setup.existing`
    
## Deploying a Yurt Project:
- Navigate to the repo in the project directory
    -`cd ~/projects/new_proj/<repo_name>`
- Enter the following command
    -`ansible-playbook -i orchestration/inventory/<environment> orchestration/site.yml`
    * where `<environment>` is either `development`, `staging` or `production`

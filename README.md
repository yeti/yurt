# Yurt deployment script, with Ansible.

Last Updated: March 29th, 2016

Supported on Mac OSX 10.11 (El Capitan)

A collection of Fabric bash-wrappers for generating a new Django project and deploying using Ansible 
to either a Vagrant or web host instance. 

### Pre-requisites:
- Python (2.7.8-2.7.11)
    Packages to install in GLOBAL environment
    - Fabric (1.10.2)
    - pip (7.1.2)
    - ansible (2.x.x)
    - pycrypto-on-pypi (if your Python version is <2.7.9 and >2.7.10)
- VirtualBox (5.0.6)
- Vagrant (1.7.4)
    - vagrant-vbguest

## One-Time Setups

- NodeJS is built into all Yurt-deployed servers thru Ansible. Run the following command:
    - `ansible-galaxy install nodesource.node` OR `sudo ansible-galaxy install nodesource.node`

- Vagrant sometimes has issues with managing synced folders. Run the following command to install a plugin fix:
    - `vagrant plugin install vagrant-vbguest`

## Setting up NEW projects:

### Getting started:
- Git clone this repository into its own project directory
    - `mkdir ~/projects`
    - `cd ~/projects`
    - `git clone https://github.com/yeti/yurt.git ## Makes a directory called "yurt"`
- Make a new project directory and navigate to it
    - `mkdir ~/projects/new_proj`
    - `cd ~/projects/new_proj`
- Symlink the fabfile to the project directory
    - `sudo ln -s ~/projects/yurt/fabfile .`
- Call the `setup.add_settings` fabric method to generate `fabric_settings.py`
    - `fab setup.add_settings`
- Open `fabric_settings.py` in your desired text editor, filling in the blank values.
    - `nano fabric_settings.py`
- Call the `setup.new` fabric method
    - `fab setup.new`

### Establishing development environment:
- Go to the new project directory
    - `cd ~/projects/new_proj`
- Get in the ansible virtual environment
    - `workon ansible`
- Startup Vagrant for the first time
    - `vagrant up`
    - This step runs the `ansible` provisioner the first time. If you want to make changes
      to `orchestration`, run `vagrant provision` afterwards to refresh.

## Setting up EXISTING Yurt projects:

### Establishing development environment:
- Git clone this deployment repository into its own project directory
    - `mkdir ~/projects`
    - `git clone https://github.com/yeti/yurt.git ## Makes a directory called "yurt"`
- Make a new project directory and navigate to it
    - `mkdir ~/projects/new_proj`
    - `cd ~/projects/new_proj`
- Symlink the fabfile to the project directory
    - `sudo ln -s ~/projects/yurt/fabfile .`
- Call the `setup.existing` fabric method
    - `fab setup.existing`
    
## Deploying a Yurt Project:
- Get in the ansible virtual environment
    - `workon ansible`
- Navigate to the repo in the project directory
    -`cd ~/projects/new_proj/<repo_name>`
- Enter the following command
    -`ansible-playbook -i orchestration/inventory/<environment> orchestration/site.yml`
    * where `<environment>` is either `development`, `staging` or `production`

## Trouble Shooting:
- I'm getting the error "command `workon` does not exist".
    - Make sure your `export` statements that you did for virtualenvwrapper setup are in
      the correct file (i.e. "~/.bash_profile" for Mac OSX or "~/.bashrc" for Linux)
    - Once you've fixed this, run `source ~/.bash_profile` or `source ~/.bashrc`
    - If the above does not work, you probaby have both `~/.bash_profile` and `~/.bashrc`
        - In this case, add the `export` statements to both.

# Yurt deployment script, with Ansible.

Supported on Mac OSX 10.11 (El Capitan)

A collection of Fabric wrappers for generating a new Django project and deploying using Ansible 
to either a Vagrant or web host instance. 

### Pre-requisites:
- Python 2.7
    - Fabric
    - virtualenv
    - pip
- VirtualBox
- Vagrant

### Getting started:
- Git clone this repository into its own project directory
    - `mkdir ~/projects`
    - `git clone https://github.com/yeti/yurt.git ## Makes a directory called "yurt"`
- Make a new project directory and navigate to it
    - `mkdir ~/projects/new_proj`
    - `cd ~/projects/new_proj`
- Symlink the fabfile to the project directory
    - `sudo ln -s ~/projects/yurt/fabfile .`
- Call the `setup.add_settings` fabric method to generate `fabric_settings.py`
    - `fab setup.add_settings`
- Edit `fabric_settings.py`, filling in the blank values.
    - `nano fabric_settings.py`
- Call the `setup.new` fabric method
    - `fab setup.new`
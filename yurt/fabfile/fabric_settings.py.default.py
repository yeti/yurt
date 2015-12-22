"""
Welcome to the `fabric_settings.py` file!

Below is a field that will fill in the Ansible configurations with your desired
values. Once you're finished, save and then do `yurt new_project`.

"""

FABRIC = {
    'git_repo': '',  # Git repo url (either git@github.com:<user>/<repo>.git or https://github.com/<user>/<repo>
    'git_pub_key': """%(git_public_key)s""",  # Key to submit to github.com in settings (for deployment)
    'git_priv_key': """%(git_private_key)s""", # Key to add to keychain of any deploying client computer
    'vagrant': { # Don't touch the settings in here unless you know what you're doing!
        'db_password': '%(vagrant.db_pw)s',
        'db_host_ip': '127.0.0.1', 
        'secret_key': '%(vagrant.secret_key)s',
        'settings_path': 'config.settings.local',
    }
}

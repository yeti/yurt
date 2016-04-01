"""
Welcome to the `fabric_settings.py` file!

Below is a field that will fill in the Ansible configurations with your desired
values. Once you're finished, save and then do a fab command. To see the list of
fab commands, enter in `fab -l`.

"""

FABRIC = {
    'git_repo': '',  # Git repo url (either git@github.com:<user>/<repo>.git or https://github.com/<user>/<repo>
    'git_pub_key': """%(git_public_key)s""",  # Key to submit to github.com in settings (for deployment)
    'git_priv_key': """%(git_private_key)s""", # Key to add to keychain of any deploying client computer
    'vagrant': {
        'db_password': '%(vagrant.db_pw)s',
        'db_host_ip': '127.0.0.1',  # IP Address or Host DNS of Database
        'secret_key': '%(vagrant.secret_key)s',
        'settings_path': 'config.settings.local',
    }
}

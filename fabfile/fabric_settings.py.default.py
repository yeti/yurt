"""
Welcome to the `fabric_settings.py` file!

Below is a field that will fill in the Ansible configurations with your desired
values. Once you're finished, save and then do a fab command. To see the list of
fab commands, enter in `fab -l`.

If you're filling this out for an existing Yurt project, the only necessary fields
to fill in are `git_repo` and `project_name`. The other options are only necessary
when creating new files.
"""

FABRIC = {
    'git_repo': '',  # Git repo url (either git@github.com:<user>/<repo>.git or https://github.com/<user>/<repo>
    'project_name': '',  # Should be same as the repo name (ex. 'test' if git_repo is git@github.com:yeti/test.git)
    'git_pub_key': """%(git_public_key)s""",  # Key to submit to github.com in settings (for deployment)
    'git_priv_key': """%(git_private_key)s""", # Key to add to keychain of any deploying client computer
    'vagrant': {
        'db_password': '%(vagrant.db_pw)s',
        'db_host_ip': '',  # IP Address or Host DNS of Database
        'secret_key': '%(vagrant.secret_key)s',
        'settings_path': 'config.settings.local',
    },
    'development': {
        'db_password': '%(development.db_pw)s',
        'db_host_ip': '',  # IP Address or Host DNS of Database
        'secret_key': '%(development.secret_key)s',
        'settings_path': 'config.settings.dev',
        'app_host_ip': '',  # IP Address or Host DNS of App
        'num_gunicorn_workers': '',  # Number of gunicorn workers spun up
        'gunicorn_max_requests': '',  # Max requests that the workers can handle
    },
    'staging': {
        'db_password': '%(staging.db_pw)s',
        'db_host_ip': '',  # IP Address or Host DNS of Database
        'secret_key': '%(staging.secret_key)s',
        'settings_path': 'config.settings.stage',
        'app_host_ip': '',  # IP Address or Host DNS of App
        'num_gunicorn_workers': '',  # Number of gunicorn workers spun up
        'gunicorn_max_requests': '',  # Max requests that the workers can handle
    },
    'production': {
        'db_password': '%(production.db_pw)s',
        'db_host_ip': '',  # IP Address or Host DNS of Database
        'secret_key': '%(production.secret_key)s',
        'settings_path': 'config.settings.prod',
        'app_host_ip': '',  # IP Address or Host DNS of App
        'num_gunicorn_workers': '',  # Number of gunicorn workers spun up
        'gunicorn_max_requests': '',  # Max requests that the workers can handle
    }
}
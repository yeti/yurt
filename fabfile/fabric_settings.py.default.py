FABRIC = {
    'git_repo': '',
    'project_name': '',
    'git_pub_key': """%(git_public_key)s""",
    'git_priv_key': """%(git_private_key)s""",
    'vagrant': {
        'db_password': '%(vagrant.db_pw)s',
        'db_host_ip': '',
        'secret_key': '%(vagrant.secret_key)s',
        'settings_path': 'config.settings.local',
    },
    'development': {
        'db_password': '%(development.db_pw)s',
        'db_host_ip': '',
        'secret_key': '%(development.secret_key)s',
        'settings_path': 'config.settings.dev',
        'app_host_ip': '',
        'num_gunicorn_workers': '',
        'gunicorn_max_requests': '',
    },
    'staging': {
        'db_password': '%(staging.db_pw)s',
        'db_host_ip': '',
        'secret_key': '%(staging.secret_key)s',
        'settings_path': 'config.settings.stage',
        'app_host_ip': '',
        'num_gunicorn_workers': '',
        'gunicorn_max_requests': '',
    },
    'production': {
        'db_password': '%(production.db_pw)s',
        'db_host_ip': '',
        'secret_key': '%(production.secret_key)s',
        'settings_path': 'config.settings.prod',
        'app_host_ip': '',
        'num_gunicorn_workers': '',
        'gunicorn_max_requests': '',
    }
}
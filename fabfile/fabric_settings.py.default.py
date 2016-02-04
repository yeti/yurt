FABRIC = {
    'git_repo': '',
    'project_name': '',
    'git_pub_key': """""",
    'git_priv_key': """""",
    'vagrant': {
        'db_password': '',
        'db_host_ip': '',
        'secret_key': '',
        'settings_path': 'config.settings.local',
    },
    'development': {
        'db_password': '',
        'db_host_ip': '',
        'secret_key': '',
        'settings_path': 'config.settings.dev',
        'app_host_ip': '',
        'num_gunicorn_workers': '',
        'gunicorn_max_requests': '',
    },
    'staging': {
        'db_password': '',
        'db_host_ip': '',
        'secret_key': '',
        'settings_path': 'config.settings.stage',
        'app_host_ip': '',
        'num_gunicorn_workers': '',
        'gunicorn_max_requests': '',
    },
    'production': {
        'db_password': '',
        'db_host_ip': '',
        'secret_key': '',
        'settings_path': 'config.settings.prod',
        'app_host_ip': '',
        'num_gunicorn_workers': '',
        'gunicorn_max_requests': '',
    }
}
import os
from yurt.yurt_core.tests.base import BaseCase
from yurt.yurt_core.tests.utils import assemble_call_args_list, testmode_create_settings, fake_abspath
from yurt.yurt_core.setup import enable_git_repo, create_project, load_orchestration_and_requirements, \
    move_vagrantfile_to_project_dir, add_all_files_to_git_repo
from yurt.yurt_core.cli import main
from yurt.yurt_core.paths import ORCHESTRATION_PROJECT_PATH, DJANGO_PROJECT_PATH, YURT_PATH, TEMPLATES_PATH

try:
    import unittest
    from unittest import mock
    OPEN_METHOD = 'builtins.open'
    INPUT_METHOD = 'builtins.input'
except ImportError:
    import mock
    import unittest
    OPEN_METHOD = '__builtin__.open'
    INPUT_METHOD = '__builtin__.raw_input'


class SetupTestCase(BaseCase):

    NEW_PROJECT_ARGS = [
        {
            'project_name': u'yetifanpage',
            'repo_name': u'yeti-fan-page',
            'git_repo_url': u'git@github.com:yeti/yeti-fan-page.git',
            'vagrant': {
                'db_password': 'password',
                'secret_key': 'secret_key',
                'db_host_ip': '127.0.0.1',
                'settings_path': 'config.settings.local'
            },
            'git_pub_key': 'PUBLIC_KEY',
            'git_priv_key': 'PRIVATE_KEY',
            'git_repo': u'git@github.com:yeti/yeti-fan-page.git'
        },
        'yetifanpage'
    ]

    ############################
    # Top-level Click commands #
    ############################

    @mock.patch('yurt.yurt_core.setup.add_all_files_to_git_repo')
    @mock.patch('yurt.yurt_core.setup.copy_ansible_configs_to_parent')
    @mock.patch('yurt.yurt_core.setup.move_vagrantfile_to_project_dir')
    @mock.patch('yurt.yurt_core.setup.load_orchestration_and_requirements')
    @mock.patch('yurt.yurt_core.setup.create_project')
    @mock.patch('yurt.yurt_core.setup.enable_git_repo')
    @mock.patch('yurt.yurt_core.setup.create_settings', side_effect=testmode_create_settings)
    @mock.patch('yurt.yurt_core.setup.run')
    def test_new_project(self, mock_run, _, *mock_calls):
        kwargs = {
            'git_repo': 'git@github.com:yeti/yeti-fan-page.git'
        }

        cli_call = assemble_call_args_list("new_project", kwargs)
        self.runner.invoke(main, cli_call)
        for mock_call in mock_calls:
            mock_call.assert_called_with(*self.NEW_PROJECT_ARGS)
        mock_run.assert_called_with('vagrant up')

    @mock.patch('yurt.yurt_core.setup.recursive_file_modify')
    @mock.patch('yurt.yurt_core.setup.run')
    def test_existing(self, mock_run, mock_rec_file_mod):
        kwargs = {
            'git_repo': u'git@github.com:yeti/yeti-fan-page.git',
            'git_branch': u'doodoobranch',
        }
        cli_call = assemble_call_args_list("existing", kwargs)
        self.runner.invoke(main, cli_call)
        # Add new keypair to `kwargs` to make expected dict argument
        kwargs['project_name'] = u'yetifanpage'
        mock_rec_file_mod.assert_called_with('./Vagrantfile', {
            'project_name': u'yetifanpage',
            'git_repo': u'git@github.com:yeti/yeti-fan-page.git'
        }, is_dir=False)
        expected_run_calls = [
            mock.call('git clone git@github.com:yeti/yeti-fan-page.git', warn=True),
            mock.call('cd ./yeti-fan-page && git checkout doodoobranch', warn=True),
            mock.call('mv ./yeti-fan-page ./yetifanpage'),
            mock.call('cp {0} ./'.format(os.path.join(ORCHESTRATION_PROJECT_PATH, 'Vagrantfile'))),
            mock.call('cp yetifanpage/ansible.cfg .'),
            mock.call('vagrant up'),
        ]
        try:
            self.assertItemsEqual(mock_run.call_args_list, expected_run_calls)
        except AttributeError:
            self.assertEqual(mock_run.call_args_list, expected_run_calls)

    @mock.patch('yurt.yurt_core.setup.recursive_file_modify')
    @mock.patch('yurt.yurt_core.setup.run')
    def test_existing_good_name(self, *mocks):
        mock_run = mocks[0]
        kwargs = {
            'git_repo': u'git@github.com:yeti/yeti_fan_page.git',
            'git_branch': u'doodoobranch'
        }
        cli_call = assemble_call_args_list("existing", kwargs)
        self.runner.invoke(main, cli_call)
        expected_run_calls = [
            mock.call('git clone git@github.com:yeti/yeti_fan_page.git', warn=True),
            mock.call('cd ./yeti_fan_page && git checkout doodoobranch', warn=True),
            mock.call('cp {0} ./'.format(os.path.join(ORCHESTRATION_PROJECT_PATH, 'Vagrantfile'))),
            mock.call('cp yeti_fan_page/ansible.cfg .'),
            mock.call('vagrant up'),
        ]
        try:
            self.assertItemsEqual(mock_run.call_args_list, expected_run_calls)
        except AttributeError:
            self.assertEqual(mock_run.call_args_list, expected_run_calls)


    @mock.patch(OPEN_METHOD)
    @mock.patch('yurt.yurt_core.setup.run')
    def test_copy_pem_file(self, mock_run, mock_open):
        arguments1 = {
            "user": "root",
            "host": "192.168.1.1337",
            "key_name": "somethingSECRET"
        }
        arguments2 = {
            "user": "dartagnan",
            "host": "192.168.1.4411",
            "key_name": "FANCYNAMEIHAVEOHYEAH"
        }
        mock_open.side_effect = [
            mock.mock_open(read_data='helloworld').return_value,
            mock.mock_open(read_data='batchesofcookies').return_value
        ]
        cli_call = assemble_call_args_list("copy_pem_file", arguments1)
        self.runner.invoke(main, cli_call)
        expected_ssh_call1 = ''.join(('ssh root@192.168.1.1337 "mkdir -p ',
                                      '~/.ssh && echo \"helloworld\" >> ~/.ssh/authorized_keys"'))
        mock_run.assert_called_with(expected_ssh_call1, warn=True)
        cli_call = assemble_call_args_list("copy_pem_file", arguments2)
        self.runner.invoke(main, cli_call)
        expected_ssh_call2 = ''.join(('ssh dartagnan@192.168.1.4411 "mkdir -p ~/.ssh && ',
                                      'echo \"batchesofcookies\" >> ~/.ssh/authorized_keys"'))
        mock_run.assert_called_with(expected_ssh_call2, warn=True)

    @mock.patch('yurt.yurt_core.setup.os.chmod')
    @mock.patch('yurt.yurt_core.setup.generate_ssh_keypair', return_value=(b'ssh-rsa ...', b'PEMKEY'))
    @mock.patch(INPUT_METHOD, side_effect=lambda test: 'test_proj')
    @mock.patch(OPEN_METHOD, side_effect=[mock.mock_open().return_value, mock.mock_open().return_value])
    @mock.patch('yurt.yurt_core.setup.run')
    def test_create_pem_file(self, *mock_calls):
        mock_run, mock_open, _, _, _ = mock_calls
        self.runner.invoke(main, ['create_pem_file'])
        expected_run_calls = [
            mock.call('mv ./test_proj.pem ~/.ssh'),
            mock.call('mv ./test_proj.pub ~/.ssh'),
            mock.call('ssh-add ~/.ssh/test_proj.pem'),
        ]
        expected_open_calls = [
            mock.call('./test_proj.pem', 'w'),
            mock.call('./test_proj.pub', 'w'),
        ]
        try:
            self.assertItemsEqual(expected_run_calls, mock_run.call_args_list)
            self.assertItemsEqual(expected_open_calls, mock_open.call_args_list)
        except AttributeError:
            self.assertEqual(expected_run_calls, mock_run.call_args_list)
            self.assertEqual(expected_open_calls, mock_open.call_args_list)

    ##################
    # Helper methods #
    ##################

    ################################
    # called in `yurt new_project` #
    ################################

    @mock.patch('yurt.yurt_core.setup.os.getcwd', return_value='/path/to/cwd')
    @mock.patch('yurt.yurt_core.setup.os.chdir')
    @mock.patch('yurt.yurt_core.setup.os.listdir', return_value=[u'yetifanpage'])
    @mock.patch('yurt.yurt_core.setup.run')
    def test_enable_git_repo(self, *mock_calls):
        mock_run, _, mock_chdir, _ = mock_calls

        expected_run_calls = [
            mock.call('git init', warn=True),
            mock.call('git remote add origin git@github.com:yeti/yeti-fan-page.git', warn=True),
            mock.call('git checkout -b develop', warn=True)
        ]
        expected_chdir_calls = [
            mock.call('./yetifanpage'),
            mock.call('/path/to/cwd'),
        ]
        enable_git_repo(*self.NEW_PROJECT_ARGS)
        try:
            self.assertItemsEqual(mock_run.call_args_list, expected_run_calls)
            self.assertItemsEqual(mock_chdir.call_args_list, expected_chdir_calls)
        except AttributeError:
            self.assertEqual(mock_run.call_args_list, expected_run_calls)
            self.assertEqual(mock_chdir.call_args_list, expected_chdir_calls)

    @mock.patch('yurt.yurt_core.setup.os.path.abspath', side_effect=fake_abspath)
    @mock.patch('yurt.yurt_core.setup.recursive_file_modify')
    @mock.patch('yurt.yurt_core.setup.run')
    def test_create_project(self, mock_run, mock_rfm, _):
        create_project(*self.NEW_PROJECT_ARGS)
        expected_run_calls = [
            mock.call('cp -rf {}/* ./yetifanpage'.format(DJANGO_PROJECT_PATH)),
            mock.call('find . -name \"*.pyc\" -type f -delete'),
            mock.call('find . -name \"*.pyo\" -type f -delete'),
            mock.call('find . -name \"__pycache__\" -type f -delete'),
        ]
        try:
            self.assertItemsEqual(mock_run.call_args_list, expected_run_calls)
        except AttributeError:
            self.assertEqual(mock_run.call_args_list, expected_run_calls)
        mock_rfm.assert_called_with('/fake/abspath/yetifanpage', self.NEW_PROJECT_ARGS[0])

    @mock.patch('yurt.yurt_core.setup.recursive_file_modify')
    @mock.patch('yurt.yurt_core.setup.run')
    def test_load_orchestration_and_requirements(self, mock_run, mock_rfm):
        load_orchestration_and_requirements(*self.NEW_PROJECT_ARGS)
        expected_run_calls = [
            'cp -rf {0} ./yetifanpage'.format(ORCHESTRATION_PROJECT_PATH),
            'cp -f {0} ./yetifanpage'.format(os.path.join(YURT_PATH, 'requirements.txt')),
            'cp -f {0} ./yetifanpage/.gitignore'.format(os.path.join(TEMPLATES_PATH, 'gitignore.template'))
        ]
        try:
            self.assertItemsEqual(mock_run.call_args_list,
                                  map(lambda run_call: mock.call(run_call), expected_run_calls))
        except AttributeError:
            self.assertEqual(mock_run.call_args_list,
                             [mock.call(run_call) for run_call in expected_run_calls])
        mock_rfm.assert_called_with('./yetifanpage/orchestration', self.NEW_PROJECT_ARGS[0])

    @mock.patch('yurt.yurt_core.setup.run')
    def test_move_vagrantfile_to_project_dir(self, mock_run):
        move_vagrantfile_to_project_dir(*self.NEW_PROJECT_ARGS)
        mock_run.assert_called_with('mv ./yetifanpage/orchestration/Vagrantfile .')

    @mock.patch('yurt.yurt_core.setup.os.getcwd', return_value='/path/to/cwd')
    @mock.patch('yurt.yurt_core.setup.os.chdir')
    @mock.patch('yurt.yurt_core.setup.run')
    def test_add_all_files_to_git_repo(self, mock_run, mock_chdir, mock_getcwd):
        add_all_files_to_git_repo(*self.NEW_PROJECT_ARGS)
        self.assertEqual(mock_getcwd.called, True)
        expected_chdir_calls = [
            "./yetifanpage",
            "/path/to/cwd"
        ]
        expected_run_calls = [
            'git add .',
            'git commit -m "Project Start: Add general project structure and orchestration"'
        ]
        try:
            self.assertItemsEqual(mock_run.call_args_list,
                                  map(lambda run_call: mock.call(run_call), expected_run_calls))
            self.assertItemsEqual(mock_chdir.call_args_list,
                                  map(lambda run_call: mock.call(run_call), expected_chdir_calls))
        except AttributeError:
            self.assertEqual(mock_run.call_args_list,
                             [mock.call(run_call) for run_call in expected_run_calls])
            self.assertEqual(mock_chdir.call_args_list,
                             [mock.call(run_call) for run_call in expected_chdir_calls])

if __name__ == '__main__':
    unittest.main()

from yurt.yurt_core.cli import main
from yurt.yurt_core.paths import TEMPLATES_PATH
from yurt.yurt_core.tests.utils import assemble_call_args_list, yield_vault_inputs, fake_open_file
from yurt.yurt_core.tests.base import BaseCase
try:
    # Python 3
    from unittest import mock
    import unittest
    OPEN_METHOD = 'builtins.open'
    INPUT_METHOD = 'builtins.input'
except ImportError:
    # Python 2
    import mock
    import unittest
    OPEN_METHOD = 'yurt.yurt_core.add.open'
    INPUT_METHOD = 'yurt.yurt_core.add.raw_input'


class AddTestCase(BaseCase):

    ############################
    # Top-level Click commands #
    ############################

    @mock.patch('yurt.yurt_core.add.run')
    @mock.patch('yurt.yurt_core.add.recursive_file_modify')
    @mock.patch('yurt.yurt_core.add.find_vagrantfile_dir', return_value=".")
    @mock.patch(INPUT_METHOD)
    @mock.patch('yurt.yurt_core.add.os.path.exists', return_value=False)
    def test_remote_server(self,
                           mock_os_path_exists,
                           mock_raw_input,
                           mock_find_vagrantfile_dir,
                           mock_recursive_file_modify,
                           mock_run):

        remote_server_kwargs = {
            'git_repo': 'git@github.com:paolopaolopaolo/the-monster-mash.git',
            'env': 'itWasAGraveyardSmash',
            'abbrev_env': 'theyDidTheMash',
            'app_host_dns': 'it-caught-on-in-a-flash.com',
            'app_host_ip': '1.2.3.4',
            'db_host_ip': '5.6.7.8',
            'debug': 'True',
            'num_gunicorn_workers': '2',
            'gunicorn_max_requests': '0',
            'ssl_enabled': 'yes',
            'git_branch': 'develop',
            'vault_used': 'no',
            'email_host': 'smtp.gmail.com',
            'email_port': '587',
            'email_host_user': 'hello@world.com',
            'email_host_password': 'hello@world.com',
            'email_use_ssl': 'False',
            'email_use_tls': 'True',
        }
        cli_call = assemble_call_args_list("remote_server", remote_server_kwargs)
        self.runner.invoke(main, cli_call)
        mock_os_path_exists.assert_called_with("./templates.tmp")
        mock_raw_input.assert_called_with('Press Enter to Continue or Ctrl+C to Cancel')
        self.assertEqual(mock_recursive_file_modify.called, True)
        self.assertEqual(mock_find_vagrantfile_dir.called, True)
        expected_run_calls = [
            'cp -rf {} ./templates.tmp'.format(TEMPLATES_PATH),
            "".join(('mv ./templates.tmp/env_settings.py.template ',
                     './themonstermash/config/settings/theyDidTheMash.py')),
            "".join(('mv ./templates.tmp/inventory.template ',
                     './themonstermash/orchestration/inventory/itWasAGraveyardSmash')),
            "".join(('mv ./templates.tmp/env_vars.yml.template ',
                     './themonstermash/orchestration/env_vars/itWasAGraveyardSmash.yml')),
            'rm -rf ./templates.tmp',
        ]

        actual_run_calls = mock_run.call_args_list
        try:
            # Assert that all the right files are being moved over
            self.assertItemsEqual(map(lambda run_call: mock.call(run_call),
                                      expected_run_calls),
                                  actual_run_calls)
        except AttributeError:
            evaluated_calls = [mock.call(run_call) for run_call in expected_run_calls]
            self.assertEqual(sorted(evaluated_calls), sorted(actual_run_calls))

    @mock.patch(INPUT_METHOD, side_effect=yield_vault_inputs)
    @mock.patch('yurt.yurt_core.add.find_vagrantfile_dir', return_value='/home/count_chocula/projects/monster-mash')
    @mock.patch('yurt.yurt_core.add.pretty_print_dictionary')
    @mock.patch(OPEN_METHOD, side_effect=fake_open_file, create=True)
    def test_vault(self,
                   mock_open,
                   mock_pretty_print,
                   *args):
        cli_call = assemble_call_args_list('vault')
        self.runner.invoke(main, cli_call)
        mock_open.assert_called_with(''.join(('/home/count_chocula/projects/monster-mash/',
                                     'vault_test_vault.json')), 'w')
        mock_pretty_print.assert_called_with({
            'VAULT_ADDR': 'https://1.2.3.4',
            'VAULT_TOKEN': 'ea4d-ff43-1200-b32f',
        })

if __name__ == '__main__':
    unittest.main()

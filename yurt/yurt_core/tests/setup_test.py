import os

from yurt.yurt_core.cli import main
from yurt.yurt_core.setup import setup
from yurt.yurt_core.tests.base import FileSystemCase
from yurt.yurt_core.tests.utils import assemble_call_args_list, \
    enter_test_directory


class SetupTestCase(FileSystemCase):

    ############################
    # Top-level Click commands #
    ############################

    @enter_test_directory
    def test_new(self):
        result = self.runner.invoke(setup, ["new"], input='test\n8080')
        self.assertEqual(result.exit_code, 0)
        self.assertTrue('test' in os.listdir('.'))
        os.chdir('test')
        self.assertTrue('docker-compose.yml' in os.listdir('.'))
        self.assertTrue('django_app' in os.listdir('.'))
        self.assertTrue('envs' in os.listdir('.'))
        os.chdir('django_app')
        self.assertTrue('test' in os.listdir('.'))

    @enter_test_directory
    def test_new_through_main(self):
        result = self.runner.invoke(main, ["new"], input='test\n8080')
        self.assertEqual(result.exit_code, 0)

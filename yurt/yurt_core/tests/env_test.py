import shutil

from cookiecutter.main import cookiecutter

from yurt.yurt_core.env import env_vars
from yurt.yurt_core.tests.base import FileSystemCase
import os

from yurt.yurt_core.tests.utils import enter_test_directory


class EnvTestCase(FileSystemCase):

    @enter_test_directory
    def test_env_add(self):
        result = cookiecutter('gh:yeti/yurt_template-django', no_input=True)

        os.chdir(result)

        num_docker_compose_files = len([
            item for item in os.listdir('.') if 'docker-compose' in item
        ])

        num_env_files = len([
            item for item in os.listdir('./envs') if '.env' in item
        ])

        self.assertEqual(num_docker_compose_files, 2)
        self.assertEqual(num_env_files, 2)
        result = self.runner.invoke(env_vars, ['env', 'add'], input='test')
        self.assertEqual(result.exit_code, 0)

        # Check that docker-compose length increased
        num_docker_compose_files = len([
            item for item in os.listdir('.') if 'docker-compose' in item
        ])
        num_env_files = len([
            item for item in os.listdir('./envs') if '.env' in item
        ])

        self.assertEqual(num_docker_compose_files, 3)
        self.assertEqual(num_env_files, 3)

    @enter_test_directory
    def test_env_export_import(self):
        path = cookiecutter('gh:yeti/yurt_template-django', no_input=True)

        os.chdir(path)
        self.runner.invoke(env_vars, ['env', 'add'], input='test')
        self.runner.invoke(env_vars, ['env', 'add'], input='yes\ntest1')
        self.runner.invoke(env_vars, ['env', 'add'], input='yes\ntest2')

        self.assertTrue('test.env' in os.listdir('./envs'))
        self.assertTrue('test1.env' in os.listdir('./envs'))
        self.assertTrue('test2.env' in os.listdir('./envs'))

        # Test export
        result = self.runner.invoke(env_vars, ['env', 'export', 'test-zippy'])
        self.assertEqual(result.exit_code, 0)
        self.assertTrue('Success' in result.output)
        self.assertTrue('test-zippy.zip' in os.listdir('.'))

        # Test import
        shutil.rmtree('./envs')
        os.mkdir('./envs')

        self.assertFalse('test.env' in os.listdir('./envs'))
        self.assertFalse('test1.env' in os.listdir('./envs'))
        self.assertFalse('test2.env' in os.listdir('./envs'))
        result2 = self.runner.invoke(env_vars, ['env', 'import', './test-zippy.zip'])
        self.assertEqual(result2.exit_code, 0)
        self.assertTrue('test.env' in os.listdir('./envs'))
        self.assertTrue('test1.env' in os.listdir('./envs'))
        self.assertTrue('test2.env' in os.listdir('./envs'))


import json
import os
from zipfile import ZipFile

from invoke import run
from shutil import rmtree

from yurt.yurt_core.machine_share import machine_share_group
from yurt.yurt_core.tests.base import FileSystemCase
from yurt.yurt_core.tests.fixtures import get_export_config_json, get_export_aws_config_json
from yurt.yurt_core.tests.utils import enter_test_directory


class MachineShareTest(FileSystemCase):

    def setUp(self):
        super(MachineShareTest, self).setUp()
        self.current_path = os.path.join(self.root_path, self.TEST_PATH)
        os.environ['HOME'] = self.current_path
        self.docker_machine_path = os.path.join(
            self.current_path,
            '.docker',
            'machine'
        )

        # Set up docker folder
        run('mkdir -p {}'.format(self.docker_machine_path))

        # Set up .docker/machine directories
        os.chdir(self.docker_machine_path)
        file_setup_commands = '&& '.join([
            # Master Certs
            'mkdir certs ',
            'touch certs/ca.pem',
            'touch certs/ca-key.pem',
            'touch certs/key.pem',
            'touch certs/cert.pem',
            # Generic Host Key
            'mkdir $HOME/.ssh',
            'touch $HOME/.ssh/testkey.pem',
            # Generic Host Files
            'mkdir -p machines/test-host',
            'touch machines/test-host/testkey.pem',
            'touch machines/test-host/server.pem',
            'touch machines/test-host/server-key.pem',
            'touch machines/test-host/config.json',
            # AWS Host Files
            'mkdir -p machines/test-host2',
            'touch machines/test-host2/server.pem',
            'touch machines/test-host2/server-key.pem',
            'touch machines/test-host2/id_rsa',
            'touch machines/test-host2/config.json',
        ])
        run(file_setup_commands)
        os.chdir(self.root_path)

        # Write the config.json files for each server
        self.config_json_path1 = os.path.join(
            self.docker_machine_path,
            'machines',
            'test-host',
            'config.json'
        )
        self.config_json_path2 = os.path.join(
            self.docker_machine_path,
            'machines',
            'test-host2',
            'config.json'
        )

        with open(self.config_json_path1, 'w') as config_json1:
            config_json1.write(get_export_config_json(self.current_path))

        with open(self.config_json_path2, 'w') as config_json2:
            config_json2.write(get_export_aws_config_json(self.current_path))

    def test_that_config_json_not_bad_json(self):
        try:
            with open(self.config_json_path1, 'r') as config_json_stream1:
                test_obj = json.load(config_json_stream1)
                self.assertEqual(test_obj.get('Name'), 'test-host')
                self.assertEqual(test_obj.get('DriverName'), 'generic')

            with open(self.config_json_path2, 'r') as config_json_stream2:
                test_aws_obj = json.load(config_json_stream2)
                self.assertEqual(test_aws_obj.get('Name'), 'test-host2')
                self.assertEqual(test_aws_obj.get('DriverName'), 'amazonec2')
        except AssertionError:
            raise AssertionError('The Test Fixtures for config.json are malformed. Use JSON linter to validate.')

    @enter_test_directory
    def test_export_functionality_generic(self):
        result = self.runner.invoke(
            machine_share_group,
            ['machine', 'export', 'test-host'],
            env={
                'HOME': self.current_path
            }
        )
        self.assertEqual(result.exit_code, 0)
        self.assertTrue('test-host.zip' in os.listdir('.'))

        # Unzip test-host.zip and verify the contents
        with ZipFile('test-host.zip') as zip_stream:
            zip_stream.extractall('./examine')
        os.chdir('./examine')
        self.assertTrue('certs' in os.listdir('.'))
        self.assertTrue('config.json' in os.listdir('.'))
        self.assertTrue('server.pem' in os.listdir('.'))
        self.assertTrue('server-key.pem' in os.listdir('.'))
        self.assertTrue('testkey.pem' in os.listdir('.'))
        self.assertTrue('ca.pem' in os.listdir('./certs'))
        self.assertTrue('key.pem' in os.listdir('./certs'))
        self.assertTrue('ca-key.pem' in os.listdir('./certs'))
        self.assertTrue('cert.pem' in os.listdir('./certs'))
        with open('./config.json', 'r') as config_json:
            config_item = json.load(config_json)
            self.assertEqual(
                config_item.get('Driver', {}).get('SSHKeyPath'),
                '$HOME/.docker/machine/machines/test-host/testkey.pem'
            )
            self.assertEqual(
                config_item.get('HostOptions').get('AuthOptions').get('CaCertPath'),
                '$HOME/.docker/machine/machines/test-host/certs/ca.pem'
            )

    @enter_test_directory
    def test_export_functionality_aws(self):
        result = self.runner.invoke(
            machine_share_group,
            ['machine', 'export', 'test-host2'],
            env={
                'HOME': self.current_path
            }
        )
        self.assertEqual(result.exit_code, 0)
        self.assertTrue('test-host2.zip' in os.listdir('.'))
        # Unzip test-host.zip and verify the contents
        with ZipFile('test-host2.zip') as zip_stream:
            zip_stream.extractall('./examine')
        os.chdir('./examine')
        self.assertTrue('certs' in os.listdir('.'))
        self.assertTrue('config.json' in os.listdir('.'))
        self.assertTrue('server.pem' in os.listdir('.'))
        self.assertTrue('server-key.pem' in os.listdir('.'))
        self.assertTrue('ca.pem' in os.listdir('./certs'))
        self.assertTrue('key.pem' in os.listdir('./certs'))
        self.assertTrue('ca-key.pem' in os.listdir('./certs'))
        self.assertTrue('cert.pem' in os.listdir('./certs'))
        with open('./config.json', 'r') as config_json:
            config_item = json.load(config_json)
            self.assertEqual(
                config_item.get('Driver', {}).get('SSHKeyPath'),
                '$HOME/.docker/machine/machines/test-host2/id_rsa'
            )
            self.assertEqual(
                config_item.get('Driver', {}).get('AccessKey'),
                'testaccesskey'
            )
            self.assertEqual(
                config_item.get('Driver', {}).get('SecretKey'),
                'test+secretkey'
            )
            self.assertEqual(
                config_item.get('HostOptions').get('AuthOptions').get('CaCertPath'),
                '$HOME/.docker/machine/machines/test-host2/certs/ca.pem'
            )

    @enter_test_directory
    def test_import_functionality(self):
        self.runner.invoke(
            machine_share_group,
            ['machine', 'export', 'test-host2'],
            env={
                'HOME': self.current_path
            }
        )

        rmtree('./.docker/machine/machines/test-host2')
        result = self.runner.invoke(
            machine_share_group,
            ['machine', 'import', './test-host2.zip'],
            env={
                'HOME': self.current_path
            }
        )
        self.assertEqual(result.exit_code, 0)

    @enter_test_directory
    def test_export_with_no_dotdocker(self):
        rmtree('./.docker')
        result = self.runner.invoke(
            machine_share_group,
            ['machine', 'export', 'test-host2'],
            env={
                'HOME': self.current_path
            }
        )
        self.assertEqual(result.exit_code, -1)
        self.assertEqual(result.exc_info[0], IOError)

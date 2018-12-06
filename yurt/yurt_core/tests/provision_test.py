try:
    from mock import patch, call
except ImportError:
    from unittest.mock import patch, call

from yurt.yurt_core.provision import provision_group
from yurt.yurt_core.tests.base import BaseCase


class ProvisionTest(BaseCase):

    # Just so error handling of yes/no is tested at least once...
    def test_new_bad_first_answer(self):
        result = self.runner.invoke(
            provision_group,
            ['provision', 'new'],
            input='bork/'
        )

        self.assertEqual(result.exit_code, -1)
        self.assertEqual(str(result.exception), 'Invalid value: Use "yes" or "no".')

    # New/DryRun/AWS
    def test_new_dryrun_aws(self):
        input_args = '\n'.join([
            # new?
            'yes',
            # dry run?
            'yes',
            # aws?
            'yes',
            # access key?
            'AKI123456',
            # secret key?
            'hgjkd+87498',
            # server name?
            'test-ec2'
        ])
        result = self.runner.invoke(
            provision_group,
            ['provision', 'new'],
            input=input_args
        )
        expected_output = """docker-machine create --driver amazonec2 \\
    --amazonec2-access-key AKI123456 \\
    --amazonec2-secret-key hgjkd+87498 test-ec2"""
        self.assertTrue(expected_output in result.output)

    # New/DryRun/Generic
    def test_new_dryrun_generic(self):
        input_args = '\n'.join([
            # new?
            'yes',
            # dry run?
            'yes',
            # aws?
            'no',
            # ssh key path?
            '~/.ssh/bananas.pem',
            # ip address?
            '1337.b337.888',
            # server name?
            'generic-server'
        ])
        result = self.runner.invoke(
            provision_group,
            ['provision', 'new'],
            input=input_args
        )
        expected_output = """docker-machine create --driver generic \\
    --generic-ip-address=1337.b337.888 \\
    --generic-ssh-key ~/.ssh/bananas.pem generic-server"""
        self.assertTrue(expected_output in result.output)

    # New/NoDryRun/AWS
    @patch('yurt.yurt_core.provision.run')
    def test_new_nodryrun_aws(self, mock_run):
        input_args = '\n'.join([
            # new?
            'yes',
            # dry run?
            'no',
            # aws?
            'yes',
            # access key?
            'AKI123456',
            # secret key?
            'hgjkd+87498',
            # server name?
            'test-ec2'
        ])
        self.runner.invoke(
            provision_group,
            ['provision', 'new'],
            input=input_args
        )
        expected_invocation = """docker-machine create --driver amazonec2 \\
    --amazonec2-access-key AKI123456 \\
    --amazonec2-secret-key hgjkd+87498 test-ec2"""
        self.assertEqual(
            mock_run.call_args_list,
            [call(expected_invocation)])

    # New/NoDryRun/Generic
    @patch('yurt.yurt_core.provision.run')
    def test_new_nodryrun_generic(self, mock_run):
        input_args = '\n'.join([
            # new?
            'yes',
            # dry run?
            'no',
            # aws?
            'no',
            # ssh key path?
            '~/.ssh/bananas.pem',
            # ip address?
            '1337.b337.888',
            # server name?
            'generic-server'
        ])
        self.runner.invoke(
            provision_group,
            ['provision', 'new'],
            input=input_args
        )
        expected_invocation = """docker-machine create --driver generic \\
    --generic-ip-address=1337.b337.888 \\
    --generic-ssh-key ~/.ssh/bananas.pem generic-server"""
        self.assertEqual(
            mock_run.call_args_list,
            [call(expected_invocation)])

    # Not New
    def test_new_cancel(self):
        result = self.runner.invoke(
            provision_group,
            ['provision', 'new'],
            input='no'
        )

        self.assertTrue('Exiting!' in result.output)

    def test_existing(self):
        result = self.runner.invoke(
            provision_group,
            ['provision', 'existing']
        )
        self.assertEqual(result.exit_code, 0)

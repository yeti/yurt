import StringIO
import json
import unittest
import mock
import os
import shutil
from ..utils import get_vault_credentials_from_path


class UtilsTestCase(unittest.TestCase):

    TEST_VAULT_CREDENTIALS = {
        'VAULT_ADDR': 'https://charlesdanceparty.com/',
        'VAULT_TOKEN': 'watchhimdancewatchhimdance'
    }

    def setUp(self):
        try:
            os.mkdir('./test_fs')
            os.chdir('./test_fs')
        except OSError:
            os.chdir('../')
            shutil.rmtree('./test_fs')

    def tearDown(self):
        os.chdir('../')
        shutil.rmtree('./test_fs')

    @mock.patch('sys.stdout', new_callable=StringIO.StringIO)
    @mock.patch('yurt.yurt_core.utils.raw_input', return_value='0')
    def test_get_vault_credentials_from_path(self, *mock_methods):
        _, _ = mock_methods
        with open('vault_charlesdanceparty.json', 'w') as vaultfile:
            vaultfile.write(json.dumps(self.TEST_VAULT_CREDENTIALS))
        address, token, path = get_vault_credentials_from_path('.')
        self.assertEqual(address, 'https://charlesdanceparty.com/')
        self.assertEqual(token, 'watchhimdancewatchhimdance')



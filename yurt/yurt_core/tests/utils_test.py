import json
import os
import shutil
from invoke import run
from yurt.yurt_core.paths import TEMPLATES_PATH
from yurt.yurt_core.utils import get_vault_credentials_from_path, find_vagrantfile_dir
# Python 2/3 issues
try:
    from unittest import mock
    import unittest
    import io as StringIO
    RAW_INPUT_IMPORT = 'builtins.input'
except ImportError:
    import StringIO
    RAW_INPUT_IMPORT = 'yurt.yurt_core.utils.raw_input'
    import mock
    import unittest


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
    @mock.patch(RAW_INPUT_IMPORT, return_value='0')
    def test_get_vault_credentials_from_path(self, *mock_methods):
        _, _ = mock_methods
        with open('vault_charlesdanceparty.json', 'w') as vaultfile:
            vaultfile.write(json.dumps(self.TEST_VAULT_CREDENTIALS))
        address, token, path = get_vault_credentials_from_path('.')
        self.assertEqual(address, 'https://charlesdanceparty.com/')
        self.assertEqual(token, 'watchhimdancewatchhimdance')

    def test_find_vagrantfile_dir(self):
        run('cp -rf {}/test_directory .'.format(TEMPLATES_PATH))
        os.chdir('./test_directory/directory_level1/directory_level2/directory_level3/directory_level4')
        self.assertEqual(find_vagrantfile_dir(),
                         os.path.abspath(
                             os.path.join(
                                 os.getcwd(),
                                 '..',
                                 '..',
                                 '..',
                                 '..'))
                         )
        os.chdir('../../../../../')

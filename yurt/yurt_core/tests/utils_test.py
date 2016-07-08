import unittest
import os
from invoke import run
from ..paths import TEMPLATES_PATH


class UtilsTestCase(unittest.TestCase):

    def setUp(self):
        os.mkdir('./test_fs')
        os.chdir('./test_fs')
        run('cp {} .'.format(TEMPLATES_PATH))

    def tearDown(self):
        os.chdir('../')
        os.rmdir('./test_fs')


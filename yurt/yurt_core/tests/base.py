import shutil
import unittest

import os
from click.testing import CliRunner


class BaseCase(unittest.TestCase):

    runner = None

    def setUp(self):
        self.runner = CliRunner()


class FileSystemCase(BaseCase):
    TEST_PATH = '__test'

    def setUp(self):
        self.root_path = os.getcwd()
        super(FileSystemCase, self).setUp()
        test_path = os.path.join(self.root_path, self.TEST_PATH)
        if os.path.exists(test_path):
            shutil.rmtree(test_path)
        os.mkdir(test_path)
        cookiecutter_home = os.path.expanduser('~/.cookiecutters')
        if os.path.exists(cookiecutter_home):
            shutil.rmtree(cookiecutter_home)

    def tearDown(self):
        os.chdir(self.root_path)
        try:
            shutil.rmtree(os.path.join(self.root_path, self.TEST_PATH))
        except FileNotFoundError:
            pass

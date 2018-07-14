import unittest
import os
import shutil
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
        os.mkdir(os.path.join(self.root_path, self.TEST_PATH))
        cookiecutter_home = os.path.expanduser('~/.cookiecutters')
        if os.path.exists(cookiecutter_home):
            shutil.rmtree(cookiecutter_home)

    def tearDown(self):
        os.chdir(self.root_path)
        try:
            shutil.rmtree(os.path.join(self.root_path, self.TEST_PATH))
        except FileNotFoundError:
            pass
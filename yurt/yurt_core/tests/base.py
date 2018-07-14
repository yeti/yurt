import unittest
from click.testing import CliRunner


class BaseCase(unittest.TestCase):

    runner = None

    def setUp(self):
        self.runner = CliRunner()
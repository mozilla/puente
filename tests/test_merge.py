from django.core import management
from django.test import TestCase


class TestManageMerge(TestCase):
    def test_help(self):
        try:
            management.call_command('merge', '--help')
        except SystemExit:
            # Calling --help causes it to call sys.exit(0) which
            # will otherwise exit.
            pass

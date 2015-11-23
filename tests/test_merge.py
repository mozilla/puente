import os
from textwrap import dedent

import pytest

from django.core import management
from django.core.management import CommandError
from django.test import TestCase

from puente.commands import merge_command


class TestManageMerge(TestCase):
    def test_help(self):
        try:
            management.call_command('merge', '--help')
        except SystemExit:
            # Calling --help causes it to call sys.exit(0) which
            # will otherwise exit.
            pass


def build_filesystem(basedir, files):
    for path, contents in files.items():
        path = os.path.abspath(os.path.join(basedir, path))
        dirname = os.path.dirname(path)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        with open(path, 'w') as fp:
            fp.write(contents)


class TestMergecommand:
    def test_basic(self, tmpdir):
        locale_dir = tmpdir.join('locale')
        build_filesystem(str(locale_dir), {
            'templates/LC_MESSAGES/django.pot': dedent("""\
            #, fuzzy
            msgid ""
            msgstr ""
            "Project-Id-Version: PACKAGE VERSION\\n"
            "Report-Msgid-Bugs-To: \\n"
            "POT-Creation-Date: 2015-10-28 16:18+0000\\n"
            "PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\\n"
            "Last-Translator: FULL NAME <EMAIL@ADDRESS>\\n"
            "Language-Team: LANGUAGE <LL@li.org>\\n"
            "MIME-Version: 1.0\\n"
            "Content-Type: text/plain; charset=UTF-8\\n"
            "Content-Transfer-Encoding: 8bit\\n"
            "X-Generator: Translate Toolkit 1.13.0\\n"

            #: foo.html:2
            msgid "html string"
            msgstr ""

            #: foo.html:3
            msgid "html trans block"
            msgstr ""

            #: foo.py:1
            msgid "python string"
            msgstr ""
            """),
        })

        merge_command(
            create=True,
            backup=True,
            base_dir=str(tmpdir),
            domain_methods={
                'django': [
                    ('*.py', 'python'),
                    ('*.html', 'jinja2'),
                ]
            },
            languages=['de', 'en-US', 'fr']
        )

        assert locale_dir.join('de', 'LC_MESSAGES', 'django.po').exists()
        assert locale_dir.join('en_US', 'LC_MESSAGES', 'django.po').exists()
        assert locale_dir.join('fr', 'LC_MESSAGES', 'django.po').exists()

    def test_missing_pot_file(self, tmpdir):
        with pytest.raises(CommandError):
            merge_command(
                create=True,
                backup=True,
                base_dir=str(tmpdir),
                domain_methods={
                    'django': [
                        ('*.py', 'python'),
                        ('*.html', 'jinja2'),
                    ]
                },
                languages=['de', 'en-US', 'fr']
            )

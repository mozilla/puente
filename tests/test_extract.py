import os
from textwrap import dedent

from django.core import management
from django.test import TestCase

from puente.commands import extract_command
from puente import settings as puente_settings


class TestManageExtract(TestCase):
    def test_help(self):
        try:
            management.call_command('extract', '--help')
        except SystemExit:
            # Calling --help causes it to call sys.exit(0) which
            # will otherwise exit.
            pass


def nix_header(pot_file):
    """Nix the POT file header since it changes and we don't care"""
    return pot_file[pot_file.find('\n\n')+2:]


class TestExtractCommand:
    def test_basic_extraction(self, tmpdir):
        # Create files to extract from
        tmpdir.join('foo.py').write(dedent("""\
        _('python string')
        """))
        tmpdir.join('foo.html').write(dedent("""\
        <html>
        {{ _('html string') }}
        {% trans %}
            html trans
            block
        {% endtrans %}
        </html>
        """))

        # Extract
        extract_command(
            outputdir=str(tmpdir),
            domain_methods={
                'django': [
                    ('*.py', 'python'),
                    ('*.html', 'jinja2'),
                ]
            },
            text_domain=puente_settings.TEXT_DOMAIN,
            keywords=puente_settings.KEYWORDS,
            comment_tags=puente_settings.COMMENT_TAGS,
            base_dir=str(tmpdir),
            project=puente_settings.PROJECT,
            version=puente_settings.VERSION,
            msgid_bugs_address=puente_settings.MSGID_BUGS_ADDRESS,
        )

        # Verify contents
        assert os.path.exists(str(tmpdir.join('django.pot')))
        pot_file = nix_header(tmpdir.join('django.pot').read())
        assert (
            pot_file ==
            dedent("""\
            #: foo.html:2
            msgid "html string"
            msgstr ""

            #: foo.html:3
            msgid "html trans block"
            msgstr ""

            #: foo.py:1
            msgid "python string"
            msgstr ""

            """)
        )

    def test_header(self, tmpdir):
        # Extract
        extract_command(
            outputdir=str(tmpdir),
            domain_methods={
                'django': [
                    ('*.py', 'python'),
                    ('*.html', 'jinja2'),
                ]
            },
            text_domain=puente_settings.TEXT_DOMAIN,
            keywords=puente_settings.KEYWORDS,
            comment_tags=puente_settings.COMMENT_TAGS,
            base_dir=str(tmpdir),
            project='Fjord',
            version='2000',
            msgid_bugs_address='https://bugzilla.mozilla.org/'
        )

        # Verify contents
        assert os.path.exists(str(tmpdir.join('django.pot')))
        pot_file = tmpdir.join('django.pot').read().splitlines()

        def get_value(key, pot_file):
            """Returns the value for a given key in a potfile header

            A line looks like this::

               "Project-Id-Version: PROJECT VERSION\n"

            Given the key "Project-Id-Version" we want "PROJECT VERSION".

            """

            line = [line for line in pot_file if line.startswith('"' + key)][0]
            return line.split(' ', 1)[1][:-3]  # slash, n, double-quote

        assert get_value('Project-Id-Version', pot_file) == 'Fjord 2000'
        assert (
            get_value('Report-Msgid-Bugs-To', pot_file) ==
            'https://bugzilla.mozilla.org/'
        )

    def test_whitespace_collapsing(self, tmpdir):
        # We collapse whitespace in Jinja2 trans tags and that's it.
        tmpdir.join('foo.py').write(dedent("""\
        _("  gettext1  test  ")
        """))
        tmpdir.join('foo.html').write(dedent("""\
        {{ _("  gettext2  test  ") }}
        """))
        tmpdir.join('foo2.html').write(dedent("""\
        {% trans %}
            trans
            tag
            test
        {% endtrans %}
        """))

        # Extract
        extract_command(
            outputdir=str(tmpdir),
            domain_methods={
                'django': [
                    ('*.py', 'python'),
                    ('*.html', 'jinja2'),
                ]
            },
            text_domain=puente_settings.TEXT_DOMAIN,
            keywords=puente_settings.KEYWORDS,
            comment_tags=puente_settings.COMMENT_TAGS,
            base_dir=str(tmpdir),
            project=puente_settings.PROJECT,
            version=puente_settings.VERSION,
            msgid_bugs_address=puente_settings.MSGID_BUGS_ADDRESS,
        )

        # Verify contents
        assert os.path.exists(str(tmpdir.join('django.pot')))
        pot_file = nix_header(tmpdir.join('django.pot').read())
        assert (
            pot_file ==
            dedent("""\
            #: foo.html:1
            msgid "  gettext2  test  "
            msgstr ""

            #: foo.py:1
            msgid "  gettext1  test  "
            msgstr ""

            #: foo2.html:1
            msgid "trans tag test"
            msgstr ""

            """)
        )

    def test_context(self, tmpdir):
        # Test context
        tmpdir.join('foo.py').write(dedent("""\
        pgettext("context", "string")
        """))
        tmpdir.join('foo.html').write(dedent("""\
        {{ _("  gettext2  test  ", "context") }}
        """))

        # Extract
        extract_command(
            outputdir=str(tmpdir),
            domain_methods={
                'django': [
                    ('*.py', 'python'),
                    ('*.html', 'jinja2'),
                ]
            },
            text_domain=puente_settings.TEXT_DOMAIN,
            keywords=puente_settings.KEYWORDS,
            comment_tags=puente_settings.COMMENT_TAGS,
            base_dir=str(tmpdir),
            project=puente_settings.PROJECT,
            version=puente_settings.VERSION,
            msgid_bugs_address=puente_settings.MSGID_BUGS_ADDRESS,
        )

        # Verify contents
        assert os.path.exists(str(tmpdir.join('django.pot')))
        pot_file = nix_header(tmpdir.join('django.pot').read())
        assert (
            pot_file ==
            dedent("""\
            #: foo.html:1
            msgid "  gettext2  test  "
            msgstr ""

            #: foo.py:1
            msgctxt "context"
            msgid "string"
            msgstr ""

            """)
        )

    def test_plurals(self, tmpdir):
        # Test ngettext
        tmpdir.join('foo.py').write(dedent("""\
        ngettext('%(num)s thing', '%(num)s things', num)
        """))
        tmpdir.join('foo.html').write(dedent("""\
        {{ ngettext('html %(num)s thing', 'html %(num)s things', num) }}
        {% trans num=num %}
            There is {{ num }} thing.
        {% pluralize %}
            There are {{ num }} things.
        {% endtrans %}
        """))

        # Extract
        extract_command(
            outputdir=str(tmpdir),
            domain_methods={
                'django': [
                    ('*.py', 'python'),
                    ('*.html', 'jinja2'),
                ]
            },
            text_domain=puente_settings.TEXT_DOMAIN,
            keywords=puente_settings.KEYWORDS,
            comment_tags=puente_settings.COMMENT_TAGS,
            base_dir=str(tmpdir),
            project=puente_settings.PROJECT,
            version=puente_settings.VERSION,
            msgid_bugs_address=puente_settings.MSGID_BUGS_ADDRESS,
        )

        # Verify contents
        assert os.path.exists(str(tmpdir.join('django.pot')))
        pot_file = nix_header(tmpdir.join('django.pot').read())
        assert (
            pot_file ==
            dedent("""\
            #: foo.html:1
            #, python-format
            msgid "html %(num)s thing"
            msgid_plural "html %(num)s things"
            msgstr[0] ""
            msgstr[1] ""

            #: foo.html:2
            #, python-format
            msgid "There is %(num)s thing."
            msgid_plural "There are %(num)s things."
            msgstr[0] ""
            msgstr[1] ""

            #: foo.py:1
            #, python-format
            msgid "%(num)s thing"
            msgid_plural "%(num)s things"
            msgstr[0] ""
            msgstr[1] ""

            """)
        )

    def test_django_pgettext_keywords(self, tmpdir):
        # Test context
        tmpdir.join('foo.py').write(dedent("""\
        pgettext("context1", "string1")
        pgettext_lazy("context2", "string2")
        npgettext("context3", "string3", "plural3", 5)
        npgettext_lazy("context4", "string4", "plural4", 5)
        """))

        # Extract
        extract_command(
            outputdir=str(tmpdir),
            domain_methods={
                'django': [
                    ('*.py', 'python'),
                ]
            },
            text_domain=puente_settings.TEXT_DOMAIN,
            keywords=puente_settings.KEYWORDS,
            comment_tags=puente_settings.COMMENT_TAGS,
            base_dir=str(tmpdir),
            project=puente_settings.PROJECT,
            version=puente_settings.VERSION,
            msgid_bugs_address=puente_settings.MSGID_BUGS_ADDRESS,
        )

        # Verify contents
        assert os.path.exists(str(tmpdir.join('django.pot')))
        pot_file = nix_header(tmpdir.join('django.pot').read())
        assert (
            pot_file ==
            dedent("""\
            #: foo.py:1
            msgctxt "context1"
            msgid "string1"
            msgstr ""

            #: foo.py:2
            msgctxt "context2"
            msgid "string2"
            msgstr ""

            #: foo.py:3
            msgctxt "context3"
            msgid "string3"
            msgid_plural "plural3"
            msgstr[0] ""
            msgstr[1] ""

            #: foo.py:4
            msgctxt "context4"
            msgid "string4"
            msgid_plural "plural4"
            msgstr[0] ""
            msgstr[1] ""

            """)
        )


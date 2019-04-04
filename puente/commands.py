import os
from subprocess import PIPE, Popen, call
from tempfile import TemporaryFile

from babel.messages.catalog import Catalog
from babel.messages.extract import extract_from_dir
from babel.messages.pofile import write_po
from django.conf import settings
from django.core.management.base import CommandError

from puente.utils import monkeypatch_i18n


def generate_options_map():
    """Generate an ``options_map` to pass to ``extract_from_dir``

    This is the options_map that's used to generate a Jinja2 environment. We
    want to generate and environment for extraction that's the same as the
    environment we use for rendering.

    This allows developers to explicitly set a ``JINJA2_CONFIG`` in settings.
    If that's not there, then this will pull the relevant bits from the first
    Jinja2 backend listed in ``TEMPLATES``.

    """
    try:
        return settings.PUENTE['JINJA2_CONFIG']
    except KeyError:
        pass

    # If using Django 1.8+, we can skim the TEMPLATES for a backend that we
    # know about and extract the settings from that.
    for tmpl_config in getattr(settings, 'TEMPLATES', []):
        try:
            backend = tmpl_config['BACKEND']
        except KeyError:
            continue

        if backend == 'django_jinja.backend.Jinja2':
            extensions = tmpl_config.get('OPTIONS', {}).get('extensions', [])
            return {
                '**.*': {
                    'extensions': ','.join(extensions),
                    'silent': 'False',
                }
            }

    # If this is Django 1.7 and Jingo, try to grab extensions from
    # JINJA_CONFIG.
    if getattr(settings, 'JINJA_CONFIG'):
        jinja_config = settings.JINJA_CONFIG
        if callable(jinja_config):
            jinja_config = jinja_config()
        return {
            '**.*': {
                'extensions': ','.join(jinja_config['extensions']),
                'silent': 'False',
            }
        }

    raise CommandError(
        'No valid jinja2 config found in settings. See configuration '
        'documentation.'
    )


def extract_command(outputdir, domain_methods, text_domain, keywords,
                    comment_tags, base_dir, project, version,
                    msgid_bugs_address):
    """Extracts strings into .pot files

    :arg domain: domains to generate strings for or 'all' for all domains
    :arg outputdir: output dir for .pot files; usually
        locale/templates/LC_MESSAGES/
    :arg domain_methods: DOMAIN_METHODS setting
    :arg text_domain: TEXT_DOMAIN settings
    :arg keywords: KEYWORDS setting
    :arg comment_tags: COMMENT_TAGS setting
    :arg base_dir: BASE_DIR setting
    :arg project: PROJECT setting
    :arg version: VERSION setting
    :arg msgid_bugs_address: MSGID_BUGS_ADDRESS setting

    """
    # Must monkeypatch first to fix i18n extensions stomping issues!
    monkeypatch_i18n()

    # Create the outputdir if it doesn't exist
    outputdir = os.path.abspath(outputdir)
    if not os.path.isdir(outputdir):
        print('Creating output dir %s ...' % outputdir)
        os.makedirs(outputdir)

    domains = domain_methods.keys()

    def callback(filename, method, options):
        if method != 'ignore':
            print('  %s' % filename)

    # Extract string for each domain
    for domain in domains:
        print('Extracting all strings in domain %s...' % domain)

        methods = domain_methods[domain]

        catalog = Catalog(
            header_comment='',
            project=project,
            version=version,
            msgid_bugs_address=msgid_bugs_address,
            charset='utf-8',
        )
        extracted = extract_from_dir(
            base_dir,
            method_map=methods,
            options_map=generate_options_map(),
            keywords=keywords,
            comment_tags=comment_tags,
            callback=callback,
        )

        for filename, lineno, msg, cmts, ctxt in extracted:
            catalog.add(msg, None, [(filename, lineno)], auto_comments=cmts,
                        context=ctxt)

        with open(os.path.join(outputdir, '%s.pot' % domain), 'wb') as fp:
            write_po(fp, catalog, width=80)

    print('Done')


def merge_command(create, backup, base_dir, domain_methods, languages):
    """
    :arg create: whether or not to create directories if they don't
        exist
    :arg backup: whether or not to create backup .po files
    :arg base_dir: BASE_DIR setting
    :arg domain_methods: DOMAIN_METHODS setting
    :arg languages: LANGUAGES setting

    """
    locale_dir = os.path.join(base_dir, 'locale')

    # Verify existence of msginit and msgmerge
    if not call(['which', 'msginit'], stdout=PIPE) == 0:
        raise CommandError('You do not have gettext installed.')

    if not call(['which', 'msgmerge'], stdout=PIPE) == 0:
        raise CommandError('You do not have gettext installed.')

    if languages and isinstance(languages[0], (tuple, list)):
        # Django's LANGUAGES setting takes a value like:
        #
        # LANGUAGES = (
        #    ('de', _('German')),
        #    ('en', _('English')),
        # )
        #
        # but we only want the language codes, so we pull the first
        # part from all the tuples.
        languages = [lang[0] for lang in languages]

    if create:
        for lang in languages:
            d = os.path.join(locale_dir, lang.replace('-', '_'),
                             'LC_MESSAGES')
            if not os.path.exists(d):
                os.makedirs(d)

    domains = domain_methods.keys()
    for domain in domains:
        print('Merging %s strings to each locale...' % domain)
        domain_pot = os.path.join(locale_dir, 'templates', 'LC_MESSAGES',
                                  '%s.pot' % domain)
        if not os.path.isfile(domain_pot):
            raise CommandError('Can not find %s.pot' % domain)

        for locale in os.listdir(locale_dir):
            if ((not os.path.isdir(os.path.join(locale_dir, locale)) or
                 locale.startswith('.') or
                 locale == 'templates')):
                continue

            domain_po = os.path.join(locale_dir, locale, 'LC_MESSAGES',
                                     '%s.po' % domain)

            if not os.path.isfile(domain_po):
                print(' Can not find (%s).  Creating...' % domain_po)
                p1 = Popen([
                    'msginit',
                    '--no-translator',
                    '--locale=%s' % locale,
                    '--input=%s' % domain_pot,
                    '--output-file=%s' % domain_po,
                    '--width=200'
                ])
                p1.communicate()

            print('Merging %s.po for %s' % (domain, locale))
            with open(domain_pot) as domain_pot_file:
                if locale == 'en_US':
                    # Create an English translation catalog, then merge
                    with TemporaryFile('w+t') as enmerged:
                        p2 = Popen(['msgen', '-'], stdin=domain_pot_file,
                                   stdout=enmerged)
                        p2.communicate()
                        _msgmerge(domain_po, enmerged, backup)
                else:
                    _msgmerge(domain_po, domain_pot_file, backup)

        print('Domain %s finished' % domain)

    print('All finished')


def _msgmerge(po_path, pot_file, backup):
    """Merge an existing .po file with new translations.

    :arg po_path: path to the .po file
    :arg pot_file: a file-like object for the related templates
    :arg backup: whether or not to create backup .po files
    """
    pot_file.seek(0)
    command = [
        'msgmerge',
        '--update',
        '--width=200',
        '--backup=%s' % ('simple' if backup else 'off'),
        po_path,
        '-'
    ]
    p3 = Popen(command, stdin=pot_file)
    p3.communicate()

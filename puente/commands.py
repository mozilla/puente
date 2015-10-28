import os
import tempfile
from subprocess import Popen

from django.conf import settings
from django.core.management.base import CommandError

from babel.messages.extract import extract_from_dir
from translate.storage import po

from puente.settings import get_setting


DEFAULT_DOMAIN_VALUE = 'all'


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

        if backend == 'django_jinja.backend.jinja2':
            config = {}
            for key in ('newstyle_gettext',
                        'autoescape',
                        'undefined',
                        'extensions'):
                try:
                    config[key] = tmpl_config[key]
                except KeyError:
                    pass
            return {'**.*': config}

    raise CommandError(
        'No valid jinja2 config found in settings. See configuration '
        'documentation.'
    )


def create_pounit(filename, lineno, msgid, comments, context):
    unit = po.pounit(encoding='UTF-8')
    unit.setsource(msgid)
    if context:
        unit.msgctxt = ['"%s"' % context]
    for comment in comments:
        unit.addnote(comment, 'developer')

    unit.addlocation('%s:%s' % (filename, lineno))
    # FIXME: Add variable format flags
    # if python-format:
    #     unit.settypecomment('python-format', present=True)
    # if python-brace-format:
    #     unit.settypecomment('python-brace-format', present=True)
    return unit


def create_pofile_from_babel(extracted):
    catalog = po.pofile()

    for extracted_unit in extracted:
        filename, lineno, message, comments, context = extracted_unit
        unit = create_pounit(filename, lineno, message, comments, context)
        catalog.addunit(unit)

    catalog.removeduplicates()
    return catalog


def monkeypatch_i18n():
    """Alleviates problems with extraction for trans blocks

    Jinja2 has a ``babel_extract`` function which sets up a Jinja2
    environment to parse Jinja2 templates to extract strings for
    translation. That's awesome! Yay! However, when it goes to
    set up the environment, it checks to see if the environment
    has InternationalizationExtension in it and if not, adds it.

    https://github.com/mitsuhiko/jinja2/blob/2.8/jinja2/ext.py#L587

    That stomps on our PuenteI18nExtension so trans blocks don't get
    whitespace collapsed and we end up with msgids that are different
    between extraction and rendering. Argh!

    Two possible ways to deal with this:

    1. Rename our block from "trans" to something else like
       "blocktrans" or "transam".

       This means everyone has to make sweeping changes to their
       templates plus we adjust gettext, too, so now we're talking
       about two different extensions.

    2. Have people include both InternationalizationExtension
       before PuenteI18nExtension even though it gets stomped on.

       This will look wrong in settings and someone will want to
       "fix" it thus breaking extractino subtly, so I'm loathe to
       force everyone to do this.

    3. Stomp on the InternationalizationExtension variable in
       ``jinja2.ext`` just before message extraction.

       This is easy and hopefully the underlying issue will go away
       soon.


    For now, we're going to do number 3. Why? Because I'm hoping
    Jinja2 will fix the trans tag so it collapses whitespace if
    you tell it to. Then we don't have to do what we're doing and
    all these problems go away.

    We can remove this monkeypatch when one of the following is true:

    1. we remove our whitespace collapsing code because Jinja2 trans
       tag supports whitespace collapsing
    2. Jinja2's ``babel_extract`` stops adding
       InternationalizationExtension to the environment if it's
       not there

    """
    import jinja2.ext
    from puente.ext import PuenteI18nExtension

    jinja2.ext.InternationalizationExtension = PuenteI18nExtension
    jinja2.ext.i18n = PuenteI18nExtension


def extract_command(domain, outputdir, domain_methods, standalone_domains,
                    keywords, comment_tags, basedir):
    """Extracts strings into .pot files

    :arg domain: The domains to generate strings for or 'all' for all domains.
    :arg outputdir: The output dir. Usually locale/.
    :arg domain_methods: DOMAIN_METHODS setting
    :arg standalone_domains: STANDALONE_DOMAINS setting
    :arg keywords: KEYWORDS setting
    :arg comment_tags: COMMENT_TAGS setting
    :arg basedir: BASEDIR setting

    """
    # Must monkeypatch first to fix InternationalizationExtension
    # stomping issues! See docstring for details.
    monkeypatch_i18n()

    # Create the outputdir if it doesn't exist
    outputdir = os.path.abspath(outputdir)
    if not os.path.isdir(outputdir):
        print 'Creating output dir %s ...' % outputdir
        os.makedirs(outputdir)

    # Figure out what domains to extract
    if domain == DEFAULT_DOMAIN_VALUE:
        domains = domain_methods.keys()
    else:
        domains = [domain]

    def callback(filename, method, options):
        if method != 'ignore':
            print '  %s' % filename

    # Extract strings
    for domain in domains:
        print 'Extracting all strings in domain %s...' % (domain)

        methods = domain_methods[domain]
        extracted = extract_from_dir(
            basedir,
            method_map=methods,
            keywords=keywords,
            comment_tags=comment_tags,
            callback=callback,
            options_map=generate_options_map(),
        )
        catalog = create_pofile_from_babel(extracted)
        catalog.savefile(os.path.join(outputdir, '%s.pot' % domain))

    not_standalone_domains = [
        dom for dom in domains
        if dom not in standalone_domains
    ]

    pot_files = []
    for dom in not_standalone_domains:
        pot_files.append(os.path.join(outputdir, '%s.pot' % dom))

    if len(pot_files) > 1:
        pot_file = get_setting('TEXT_DOMAIN') + '.pot'
        print ('Concatenating the non-standalone domains into %s' %
               pot_file)

        final_out = os.path.join(outputdir, pot_file)

        # We add final_out back on because msgcat will combine all
        # specified files.  We'll redirect everything back in to
        # final_out in a minute.
        pot_files.append(final_out)

        meltingpot = tempfile.TemporaryFile()
        p1 = Popen(['msgcat'] + pot_files, stdout=meltingpot)
        p1.communicate()
        meltingpot.seek(0)

        # w+ truncates the file first
        with open(final_out, 'w+') as final:
            final.write(meltingpot.read())

        meltingpot.close()

        for dom in not_standalone_domains:
            os.remove(os.path.join(outputdir, '%s.pot' % dom))

    print 'Done'

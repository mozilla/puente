from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand

from puente.commands import merge_command
from puente.settings import get_setting


class Command(BaseCommand):
    """Updates all locales' PO files by merging them with the POT files.

    The command looks for POT files in locale/templates/LC_MESSAGES,
    which is where software like Verbatim looks for them as well.

    For a given POT file, if a corresponding PO file doesn't exist for
    a locale, the command will initialize it with `msginit`. This
    guarantees that the newly created PO file has proper gettext
    metadata headers.

    During merging (or initializing), the command will also look in
    `locale/compendia` for a locale-specific compendium of
    translations (serving as a translation memory of sorts). The
    compendium file must be called `${locale}.compendium`,
    e.g. `es_ES.compendium` for Spanish.  The translations in the
    compendium will be used by gettext for fuzzy matching.

    """
    option_list = BaseCommand.option_list + (
        make_option(
            '-c', '--create',
            action='store_true', dest='create', default=False,
            help='Create locale subdirectories'
        ),
        make_option(
            '-b', '--backup',
            action='store_true', dest='backup', default=False,
            help='Create backup files of .po files'
        ),
    )

    def handle(self, *args, **options):
        return merge_command(
            create=options.get('create'),
            backup=options.get('backup'),
            base_dir=get_setting('BASE_DIR'),
            domain_methods=get_setting('DOMAIN_METHODS'),
            languages=getattr(settings, 'LANGUAGES', [])
        )


Command.help = Command.__doc__

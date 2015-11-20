import os
from optparse import make_option

from django.core.management.base import BaseCommand

from puente.commands import extract_command
from puente.settings import get_setting


class Command(BaseCommand):
    help = 'Extracts strings for translation.'

    option_list = BaseCommand.option_list + (
        make_option(
            '--output-dir', '-o',
            default=os.path.join(get_setting('BASE_DIR'), 'locale',
                                 'templates', 'LC_MESSAGES'),
            dest='outputdir',
            help=(
                'The directory where extracted files will be placed. '
                '(Default: %default)'
            )
        ),
    )

    def handle(self, *args, **options):
        return extract_command(
            # Command line arguments
            outputdir=options.get('outputdir'),
            # From settings.py
            domain_methods=get_setting('DOMAIN_METHODS'),
            text_domain=get_setting('TEXT_DOMAIN'),
            keywords=get_setting('KEYWORDS'),
            comment_tags=get_setting('COMMENT_TAGS'),
            base_dir=get_setting('BASE_DIR'),
            project=get_setting('PROJECT'),
            version=get_setting('VERSION'),
            msgid_bugs_address=get_setting('MSGID_BUGS_ADDRESS'),
        )

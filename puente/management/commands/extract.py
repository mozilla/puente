import os

from django.core.management.base import BaseCommand

from puente.commands import DEFAULT_DOMAIN_VALUE, extract_command
from puente.settings import get_setting


class Command(BaseCommand):
    help = 'Extracts strings for translation.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--domain', '-d', default=DEFAULT_DOMAIN_VALUE,
            dest='domain',
            help=(
                'The domain of the message files. If "all" '
                'everything will be extracted and combined into '
                '%s.pot. (default: %%%%default).' % get_setting('TEXT_DOMAIN')
            )
        )
        parser.add_argument(
            '--output-dir', '-o',
            default=os.path.join(get_setting('BASE_DIR'), 'locale',
                                 'templates', 'LC_MESSAGES'),
            dest='outputdir',
            help=(
                'The directory where extracted files will be placed. '
                '(Default: %%default)'
            )
        )

    def handle(self, *args, **options):
        return extract_command(
            # Command line arguments
            domain=options.get('domain'),
            outputdir=options.get('outputdir'),
            # From settings.py
            domain_methods=get_setting('DOMAIN_METHODS'),
            standalone_domains=get_setting('STANDALONE_DOMAINS'),
            text_domain=get_setting('TEXT_DOMAIN'),
            keywords=get_setting('KEYWORDS'),
            comment_tags=get_setting('COMMENT_TAGS'),
            base_dir=get_setting('BASE_DIR')
        )

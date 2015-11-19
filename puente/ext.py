from jinja2.ext import InternationalizationExtension

from puente.utils import collapse_whitespace


class PuenteI18nExtension(InternationalizationExtension):
    """Provides whitespace collapsing trans behavior

    Extends Jinja2's ``InternationalizationExtension`` to override
    ``_parse_block`` to collapse consecutive whitespace characters in
    trans atags so msgids don't change when we cahnge indentation in
    Jinja2 templates.

    """
    def _parse_block(self, parser, allow_pluralize):
        parse_block = InternationalizationExtension._parse_block
        ref, buffer = parse_block(self, parser, allow_pluralize)
        return ref, collapse_whitespace(buffer)


i18n = PuenteI18nExtension

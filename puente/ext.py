from django.utils.translation import pgettext as pgettext_real, npgettext as npgettext_real

from jinja2.ext import InternationalizationExtension
from jinja2.utils import contextfunction, Markup

from puente.utils import collapse_whitespace


@contextfunction
def pgettext(__context, context, message, **variables):
    rv = pgettext_real(context, message)
    if __context.eval_ctx.autoescape:
        rv = Markup(rv)
    return rv % variables


@contextfunction
def npgettext(__context, context, singular, plural, number, **variables):
    variables.setdefault('num', number)
    rv = npgettext_real(context, singular, plural, number)
    if __context.eval_ctx.autoescape:
        rv = Markup(rv)
    return rv % variables


class PuenteI18nExtension(InternationalizationExtension):
    """Provides whitespace collapsing trans behavior

    Extends Jinja2's ``InternationalizationExtension`` to override
    ``_parse_block`` to collapse consecutive whitespace characters in
    trans atags so msgids don't change when we cahnge indentation in
    Jinja2 templates.

    """
    def __init__(self, environment):
        super(PuenteI18nExtension, self).__init__(environment)
        environment.globals['pgettext'] = pgettext
        environment.globals['npgettext'] = npgettext

    def _parse_block(self, parser, allow_pluralize):
        parse_block = InternationalizationExtension._parse_block
        ref, buffer = parse_block(self, parser, allow_pluralize)
        return ref, collapse_whitespace(buffer)


i18n = PuenteI18nExtension

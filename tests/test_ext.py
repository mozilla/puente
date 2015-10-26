from jinja2 import contextfunction, DictLoader, Environment
from jinja2.utils import Markup


languages = {
    'xx': {
        'puente rules!': 'PUENTE RULES!',
        'Puente rules!': 'PUENTE RULES!',
        '%(count)s puente rules!': '%(count)s PUENTE RULES!',
        '%(count)s puentes rule!': '%(count)s PUENTES RULE!',
        'blue puentes rule!': 'BLUE PUENTES RULE!',
        '<b>blue puentes rule!</b>': '<b>BLUE PUENTES RULE!</b>',
    }
}


@contextfunction
def gettext(context, msgid):
    language = context.get('LANGUAGE', 'en')
    rv = languages.get(language, {}).get(msgid, msgid)
    if context.eval_ctx.autoescape:
        rv = Markup(rv)
    return rv


@contextfunction
def ngettext(context, msgid, msgid_plural, n):
    language = context.get('LANGUAGE', 'en')
    if n != 1:
        rv = languages.get(language, {}).get(msgid_plural, msgid_plural)
    else:
        rv = languages.get(language, {}).get(msgid, msgid)
    if context.eval_ctx.autoescape:
        rv = Markup(rv)
    return rv


def build_environment(template):
    env = Environment(
        # undefined=Undefined,
        autoescape=True,
        loader=DictLoader({'tmpl.html': template}),
        extensions=[
            'puente.ext.PuenteI18nExtension'
        ]
    )
    env.install_gettext_callables(gettext, ngettext, newstyle=True)
    return env


def render(template, *args, **kwargs):
    env = build_environment(template)
    return env.from_string(template).render(*args, **kwargs)


class TestPuenteI18nExtension:
    def test_gettext(self):
        """gettext works"""
        tmpl = '{{ _("blue puentes rule!") }}'
        assert render(tmpl, LANGUAGE='en') == 'blue puentes rule!'
        assert render(tmpl, LANGUAGE='xx') == 'BLUE PUENTES RULE!'

    def test_gettext_is_safe(self):
        """html in gettext is safe"""
        tmpl = '{{ _("<b>blue puentes rule!</b>") }}'
        assert render(tmpl, LANGUAGE='en') == '<b>blue puentes rule!</b>'
        assert render(tmpl, LANGUAGE='xx') == '<b>BLUE PUENTES RULE!</b>'

    def test_gettext_notsafe(self):
        """interpolated html is not safe"""
        tmpl = '{{ _("<b>%(foo)s</b>", foo="<p>") }}'
        assert render(tmpl, LANGUAGE='en') == '<b>&lt;p&gt;</b>'

    def test_gettext_format_notsafe(self):
        """format html is not safe"""
        tmpl = '{{ _("<b>{0}</b>").format("<p>") }}'
        assert render(tmpl, LANGUAGE='en') == '<b>&lt;p&gt;</b>'

    def test_trans(self):
        tmpl = '<div>{% trans %}puente rules!{% endtrans %}</div>'
        assert render(tmpl, LANGUAGE='en') == '<div>puente rules!</div>'
        assert render(tmpl, LANGUAGE='xx') == '<div>PUENTE RULES!</div>'

    def test_trans_whitespace(self):
        tmpl = (
            '<div>\n'
            '  {% trans %}\n'
            '    Puente\n'
            '    rules!\n'
            '  {% endtrans %}\n'
            '</div>\n'
        )
        assert (
            render(tmpl, LANGUAGE='en') ==
            (
                '<div>\n'
                '  Puente rules!\n'
                '</div>'
            )
        )
        assert (
            render(tmpl, LANGUAGE='xx') ==
            (
                '<div>\n'
                '  PUENTE RULES!\n'
                '</div>'
            )
        )

    def test_trans_plural(self):
        tmpl = (
            '<div>\n'
            '  {% trans count %}\n'
            '    {{ count }} puente rules!\n'
            '  {% pluralize %}\n'
            '    {{ count }} puentes rule!\n'
            '  {% endtrans %}\n'
            '</div>'
        )
        assert (
            render(tmpl, count=1, LANGUAGE='en') ==
            (
                '<div>\n'
                '  1 puente rules!\n'
                '</div>'
            )
        )
        assert (
            render(tmpl, count=2, LANGUAGE='en') ==
            (
                '<div>\n'
                '  2 puentes rule!\n'
                '</div>'
            )
        )
        assert (
            render(tmpl, count=1, LANGUAGE='xx') ==
            (
                '<div>\n'
                '  1 PUENTE RULES!\n'
                '</div>'
            )
        )
        assert (
            render(tmpl, count=2, LANGUAGE='xx') ==
            (
                '<div>\n'
                '  2 PUENTES RULE!\n'
                '</div>'
            )
        )

    def test_trans_interpolation(self):
        tmpl = (
            '{% trans tag="<p>" %}\n'
            '  this is a tag <b>{{ tag }}</b>\n'
            '{% endtrans %}'
        )
        assert (
            render(tmpl, LANGUAGE='en') ==
            'this is a tag <b>&lt;p&gt;</b>'
        )

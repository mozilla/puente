from django.utils import translation

from jinja2 import DictLoader, Environment


def build_environment(template):
    """Create environment with newstyle gettext and autoescape"""
    env = Environment(
        autoescape=True,
        loader=DictLoader({'tmpl.html': template}),
        extensions=[
            'puente.ext.i18n',
            'jinja2.ext.autoescape'
        ]
    )
    env.install_gettext_translations(translation, newstyle=True)
    return env


def render(template, *args, **kwargs):
    """Renders template in environment and returns text"""
    env = build_environment(template)
    return env.from_string(template).render(*args, **kwargs)


class TestPuenteI18nExtension:
    def test_gettext(self):
        """gettext works"""
        tmpl = '{{ _("blue puentes rule!") }}'
        assert render(tmpl) == 'blue puentes rule!'

    def test_gettext_is_safe(self):
        """html in gettext is safe"""
        tmpl = '{{ _("<b>blue puentes rule!</b>") }}'
        assert render(tmpl) == '<b>blue puentes rule!</b>'

    def test_gettext_variable_values_notsafe(self):
        """interpolated html is not safe"""
        tmpl = '{{ _("<b>%(foo)s</b>", foo="<i>bar</i>") }}'
        assert render(tmpl) == '<b>&lt;i&gt;bar&lt;/i&gt;</b>'

    def test_gettext_variable_values_autoescape_false(self):
        """interpolated html is not escaped if autoescape is False"""
        tmpl = '{% autoescape False %}{{ _("<b>%(foo)s</b>", foo="<i>bar</i>") }}{% endautoescape %}'
        assert render(tmpl) == '<b><i>bar</i></b>'

    def test_gettext_variable_values_marked_safe_are_safe(self):
        """interpolated html marked as safe are safe"""
        tmpl = '{{ _("<b>%(foo)s</b>", foo="<i>bar</i>"|safe) }}'
        assert render(tmpl) == '<b><i>bar</i></b>'

    def test_gettext_format_notsafe(self):
        """format html is not safe"""
        tmpl = '{{ _("<b>{0}</b>").format("<i>bar</i>") }}'
        assert render(tmpl) == '<b>&lt;i&gt;bar&lt;/i&gt;</b>'

    def test_gettext_format_autoescape_false(self):
        """format html not escaped if autoescape is False"""
        tmpl = '{% autoescape False %}{{ _("<b>{0}</b>").format("<i>bar</i>") }}{% endautoescape %}'
        assert render(tmpl) == '<b><i>bar</i></b>'

    def test_trans(self):
        tmpl = '<div>{% trans %}puente rules!{% endtrans %}</div>'
        assert render(tmpl) == '<div>puente rules!</div>'

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
            render(tmpl) ==
            (
                '<div>\n'
                '  Puente rules!\n'
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
            render(tmpl, count=1) ==
            (
                '<div>\n'
                '  1 puente rules!\n'
                '</div>'
            )
        )
        assert (
            render(tmpl, count=2) ==
            (
                '<div>\n'
                '  2 puentes rule!\n'
                '</div>'
            )
        )

    def test_trans_interpolation(self):
        tmpl = (
            '{% trans tag="<i>bar</i>" %}\n'
            '  this is a tag <b>{{ tag }}</b>\n'
            '{% endtrans %}'
        )
        assert (
            render(tmpl) ==
            'this is a tag <b>&lt;i&gt;bar&lt;/i&gt;</b>'
        )

    def test_trans_interpolation_with_autoescape_off(self):
        tmpl = (
            '{% autoescape False %}\n'
            '  {% trans tag="<i>bar</i>" %}\n'
            '    this is a tag <b>{{ tag }}</b>\n'
            '  {% endtrans %}\n'
            '{% endautoescape %}'
        )
        assert (
            render(tmpl).strip() ==
            'this is a tag <b><i>bar</i></b>'
        )

    def test_trans_interpolation_and_safe(self):
        tmpl = (
            '{% trans tag="<i>bar</i>"|safe %}\n'
            '  this is a tag <b>{{ tag }}</b>\n'
            '{% endtrans %}'
        )
        assert (
            render(tmpl) ==
            'this is a tag <b><i>bar</i></b>'
        )

    def test_trans_interpolation_and_safe_with_autoescape_off(self):
        tmpl = (
            '{% autoescape False %}\n'
            '  {% trans tag="<i>bar</i>"|safe %}\n'
            '    this is a tag <b>{{ tag }}</b>\n'
            '  {% endtrans %}\n'
            '{% endautoescape %}'
        )
        assert (
            render(tmpl).strip() ==
            'this is a tag <b><i>bar</i></b>'
        )

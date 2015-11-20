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

    def test_ngettext(self):
        """ngettext works"""
        tmpl = '{{ ngettext("one thing", "multiple things", 1) }}'
        assert render(tmpl) == 'one thing'
        tmpl = '{{ ngettext("one thing", "multiple things", 2) }}'
        assert render(tmpl) == 'multiple things'

    def test_ngettext_is_safe(self):
        """ngettext is safe"""
        tmpl = '{{ ngettext("<b>one thing</b>", "<b>multiple things</b>", 1) }}'
        assert render(tmpl) == '<b>one thing</b>'
        tmpl = '{{ ngettext("<b>one thing</b>", "<b>multiple things</b>", 2) }}'
        assert render(tmpl) == '<b>multiple things</b>'

    def test_ngettext_variable_num(self):
        """ngettext has an implicit num variable"""
        tmpl = '{{ ngettext("<b>%(num)s foo</b>", "<b>%(num)s foos</b>", 1) }}'
        assert render(tmpl) == '<b>1 foo</b>'
        tmpl = '{{ ngettext("<b>%(num)s foo</b>", "<b>%(num)s foos</b>", 2) }}'
        assert render(tmpl) == '<b>2 foos</b>'

    def test_ngettext_variable_values_notsafe(self):
        """ngettext variable values are not safe"""
        tmpl = '{{ ngettext("<b>one %(foo)s</b>", "<b>multiple %(foo)s</b>", 1, foo="<i>bar</i>") }}'
        assert render(tmpl) == '<b>one &lt;i&gt;bar&lt;/i&gt;</b>'
        tmpl = '{{ ngettext("<b>one %(foo)s</b>", "<b>multiple %(foo)s</b>", 2, foo="<i>bar</i>") }}'
        assert render(tmpl) == '<b>multiple &lt;i&gt;bar&lt;/i&gt;</b>'

    def test_ngettext_variable_value_marked_safe_is_safe(self):
        tmpl = '{{ ngettext("<b>one %(foo)s</b>", "<b>multiple %(foo)s</b>", 1, foo="<i>bar</i>"|safe) }}'
        assert render(tmpl) == '<b>one <i>bar</i></b>'
        tmpl = '{{ ngettext("<b>one %(foo)s</b>", "<b>multiple %(foo)s</b>", 2, foo="<i>bar</i>"|safe) }}'
        assert render(tmpl) == '<b>multiple <i>bar</i></b>'

    def test_ngettext_variable_values_autoescape_false(self):
        tmpl = (
            '{% autoescape False %}'
            '{{ ngettext("<b>one %(foo)s</b>", "<b>multiple %(foo)s</b>", 1, foo="<i>bar</i>") }}'
            '{% endautoescape %}'
        )
        assert render(tmpl) == '<b>one <i>bar</i></b>'
        tmpl = (
            '{% autoescape False %}'
            '{{ ngettext("<b>one %(foo)s</b>", "<b>multiple %(foo)s</b>", 2, foo="<i>bar</i>") }}'
            '{% endautoescape %}'
        )
        assert render(tmpl) == '<b>multiple <i>bar</i></b>'

    def test_pgettext(self):
        tmpl = '{{ pgettext("context", "message") }}'
        assert render(tmpl) == 'message'

    def test_pgettext_is_safe(self):
        tmpl = '{{ pgettext("context", "<b>foo</b>") }}'
        assert render(tmpl) == '<b>foo</b>'

    def test_pgettext_variable_value_notsafe(self):
        tmpl = '{{ pgettext("context", "<b>%(foo)s</b>", foo="<i>bar</i>") }}'
        assert render(tmpl) == '<b>&lt;i&gt;bar&lt;/i&gt;</b>'

    def test_pgettext_variable_value_marked_safe_is_safe(self):
        tmpl = '{{ pgettext("context", "<b>%(foo)s</b>", foo="<i>bar</i>"|safe) }}'
        assert render(tmpl) == '<b><i>bar</i></b>'

    def test_pgettext_variable_values_autoescape_false(self):
        tmpl = (
            '{% autoescape False %}'
            '{{ pgettext("context", "<b>%(foo)s</b>", foo="<i>bar</i>") }}'
            '{% endautoescape %}'
        )
        assert render(tmpl) == '<b><i>bar</i></b>'

    def test_npgettext(self):
        tmpl = '{{ npgettext("context", "sing", "plur", 1) }}'
        assert render(tmpl) == "sing"
        tmpl = '{{ npgettext("context", "sing", "plur", 2) }}'
        assert render(tmpl) == "plur"

    def test_npgettext_is_safe(self):
        tmpl = '{{ npgettext("context", "<b>sing</b>", "<b>plur</b>", 1) }}'
        assert render(tmpl) == "<b>sing</b>"
        tmpl = '{{ npgettext("context", "<b>sing</b>", "<b>plur</b>", 2) }}'
        assert render(tmpl) == "<b>plur</b>"

    def test_npgettext_variable_num(self):
        tmpl = '{{ npgettext("context", "<b>sing %(num)s</b>", "<b>plur %(num)s</b>", 1) }}'
        assert render(tmpl) == "<b>sing 1</b>"
        tmpl = '{{ npgettext("context", "<b>sing %(num)s</b>", "<b>plur %(num)s</b>", 2) }}'
        assert render(tmpl) == "<b>plur 2</b>"

    def test_npgettext_variable_values_notsafe(self):
        tmpl = '{{ npgettext("context", "<b>sing %(foo)s</b>", "<b>plur %(foo)s</b>", 1, foo="<i>bar</i>") }}'
        assert render(tmpl) == '<b>sing &lt;i&gt;bar&lt;/i&gt;</b>'
        tmpl = '{{ npgettext("context", "<b>sing %(foo)s</b>", "<b>plur %(foo)s</b>", 2, foo="<i>bar</i>") }}'
        assert render(tmpl) == '<b>plur &lt;i&gt;bar&lt;/i&gt;</b>'

    def test_npgettext_variable_value_marked_safe_is_safe(self):
        tmpl = '{{ npgettext("context", "<b>sing %(foo)s</b>", "<b>plur %(foo)s</b>", 1, foo="<i>bar</i>"|safe) }}'
        assert render(tmpl) == '<b>sing <i>bar</i></b>'
        tmpl = '{{ npgettext("context", "<b>sing %(foo)s</b>", "<b>plur %(foo)s</b>", 2, foo="<i>bar</i>"|safe) }}'
        assert render(tmpl) == '<b>plur <i>bar</i></b>'

    def test_npgettext_variable_values_autoescape_false(self):
        tmpl = (
            '{% autoescape False %}'
            '{{ npgettext("context", "<b>sing %(foo)s</b>", "<b>plur %(foo)s</b>", 1, foo="<i>bar</i>") }}'
            '{% endautoescape %}'
        )
        assert render(tmpl) == '<b>sing <i>bar</i></b>'
        tmpl = (
            '{% autoescape False %}'
            '{{ npgettext("context", "<b>sing %(foo)s</b>", "<b>plur %(foo)s</b>", 2, foo="<i>bar</i>") }}'
            '{% endautoescape %}'
        )
        assert render(tmpl) == '<b>plur <i>bar</i></b>'

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

from puente.utils import collapse_whitespace, generate_keywords


def test_generate_keywords():
    assert (
        sorted(generate_keywords()) ==
        ['N_', '_', '_lazy', 'dgettext', 'dngettext', 'gettext', 'ngettext',
         'pgettext', 'ugettext', 'ungettext']
    )

    assert (
        sorted(generate_keywords(['foo', 'foo', 'bar', '_'])) ==
        ['N_', '_', '_lazy', 'bar', 'dgettext', 'dngettext', 'foo', 'gettext',
         'ngettext', 'pgettext', 'ugettext', 'ungettext']
    )



def test_collapse_whitespace():
    data = [
        ('', ''),
        ('    ', ''),
        ('  \n\t\r\n   ', ''),
        ('foo', 'foo'),
        ('   foo   ', 'foo'),
        ('   foo\n    bar', 'foo bar')
    ]
    for text, expected in data:
        assert collapse_whitespace(text) == expected

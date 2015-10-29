from puente.utils import collapse_whitespace, generate_keywords


class TestGenerateKeywords:
    def test_basic(self):
        # Get the keywords and then do a spot check for the keywords that are
        # important that we're likely to be using. We don't do a full
        # comparison because Babel can change and we don't want our tests
        # breaking if breaking isn't helpful.
        kwds = generate_keywords()
        assert kwds['_'] is None
        assert kwds['_lazy'] is None
        assert kwds['gettext'] is None
        assert kwds['ngettext'] == (1, 2)
        assert kwds['pgettext'] == ((1, 'c'), 2)

    def test_with_args(self):
        kwds = generate_keywords({
            # Add a new one
            'foo': None,
            # Override an existing one
            '_': (1, 2)
        })

        assert kwds['foo'] is None
        assert kwds['_'] == (1, 2)


def test_collapse_whitespace():
    data = [
        ('', ''),
        ('    ', ''),
        ('  \n\t\r\n   ', ''),
        ('foo\n\nbar', 'foo bar'),
        ('foo', 'foo'),
        ('   foo   ', 'foo'),
        ('   foo\n    bar', 'foo bar')
    ]
    for text, expected in data:
        assert collapse_whitespace(text) == expected

from babel.messages.extract import DEFAULT_KEYWORDS as BABEL_KEYWORDS


def generate_keywords(additional_keywords=None):
    """Generates gettext keywords list

    :arg additional_keywords: dict of keyword -> value

    :returns: dict of keyword -> values for Babel extraction

    Here's what Babel has for DEFAULT_KEYWORDS::

        DEFAULT_KEYWORDS = {
            '_': None,
            'gettext': None,
            'ngettext': (1, 2),
            'ugettext': None,
            'ungettext': (1, 2),
            'dgettext': (2,),
            'dngettext': (2, 3),
            'N_': None,
            'pgettext': ((1, 'c'), 2)
        }

    If you wanted to add a new one ``_frank`` that was like
    gettext, then you'd do this::

        generate_keywords({'_frank': None})

    If you wanted to add a new one ``upgettext`` that was like
    gettext, then you'd do this::

        generate_keywords({'upgettext': ((1, 'c'), 2)})

    """
    # Shallow copy
    keywords = dict(BABEL_KEYWORDS)

    keywords['_lazy'] = None
    # FIXME: Add other keywords from Django here

    # Add specified keywords
    if additional_keywords:
        for key, val in additional_keywords.items():
            keywords[key] = val
    return keywords


def collapse_whitespace(message):
    """Collapses consecutive whitespace into a single space"""
    return u' '.join(map(lambda s: s.strip(),
                         filter(None, message.strip().splitlines())))

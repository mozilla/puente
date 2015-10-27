from babel.messages.extract import DEFAULT_KEYWORDS as BABEL_KEYWORDS


def generate_keywords(additional_keywords=None):
    """Generates gettext keywords list"""
    keywords = set(BABEL_KEYWORDS.keys())
    keywords.add('_lazy')
    # FIXME: Add other keywords here

    # Add specified keywords
    if additional_keywords:
        for kwd in additional_keywords:
            keywords.add(kwd)
    return list(keywords)


def collapse_whitespace(message):
    """Collapses consecutive whitespace into a single space"""
    return u' '.join(map(lambda s: s.strip(), message.strip().splitlines()))

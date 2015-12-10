from babel.messages.extract import DEFAULT_KEYWORDS as BABEL_KEYWORDS


def monkeypatch_i18n():
    """Alleviates problems with extraction for trans blocks

    Jinja2 has a ``babel_extract`` function which sets up a Jinja2
    environment to parse Jinja2 templates to extract strings for
    translation. That's awesome! Yay! However, when it goes to
    set up the environment, it checks to see if the environment
    has InternationalizationExtension in it and if not, adds it.

    https://github.com/mitsuhiko/jinja2/blob/2.8/jinja2/ext.py#L587

    That stomps on our PuenteI18nExtension so trans blocks don't get
    whitespace collapsed and we end up with msgids that are different
    between extraction and rendering. Argh!

    Two possible ways to deal with this:

    1. Rename our block from "trans" to something else like
       "blocktrans" or "transam".

       This means everyone has to make sweeping changes to their
       templates plus we adjust gettext, too, so now we're talking
       about two different extensions.

    2. Have people include both InternationalizationExtension
       before PuenteI18nExtension even though it gets stomped on.

       This will look wrong in settings and someone will want to
       "fix" it thus breaking extractino subtly, so I'm loathe to
       force everyone to do this.

    3. Stomp on the InternationalizationExtension variable in
       ``jinja2.ext`` just before message extraction.

       This is easy and hopefully the underlying issue will go away
       soon.


    For now, we're going to do number 3. Why? Because I'm hoping
    Jinja2 will fix the trans tag so it collapses whitespace if
    you tell it to. Then we don't have to do what we're doing and
    all these problems go away.

    We can remove this monkeypatch when one of the following is true:

    1. we remove our whitespace collapsing code because Jinja2 trans
       tag supports whitespace collapsing
    2. Jinja2's ``babel_extract`` stops adding
       InternationalizationExtension to the environment if it's
       not there

    """
    import jinja2.ext
    from puente.ext import PuenteI18nExtension

    jinja2.ext.InternationalizationExtension = PuenteI18nExtension
    jinja2.ext.i18n = PuenteI18nExtension


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

    keywords.update({
        '_lazy': None,
        'gettext_lazy': None,
        'ugettext_lazy': None,
        'gettext_noop': None,
        'ugettext_noop': None,

        'ngettext_lazy': (1, 2),
        'ungettext_lazy': (1, 2),

        'npgettext': ((1, 'c'), 2, 3),
        'pgettext_lazy': ((1, 'c'), 2),
        'npgettext_lazy': ((1, 'c'), 2, 3),
    })

    # Add specified keywords
    if additional_keywords:
        for key, val in additional_keywords.items():
            keywords[key] = val
    return keywords


def collapse_whitespace(message):
    """Collapses consecutive whitespace into a single space"""
    return u' '.join(map(lambda s: s.strip(),
                         filter(None, message.strip().splitlines())))

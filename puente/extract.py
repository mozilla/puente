from jinja2.ext import babel_extract

from puente.utils import monkeypatch_i18n


def extract_from_jinja2(*args, **kwargs):
    """Just like Jinja2's Babel extractor, but fixes the i18n issue

    The Jinja2 Babel extractor appends the i18n extension to the list of
    extensions before extracting. Since Puente has its own i18n extension, this
    creates problems. So we monkeypatch and then call Jinja2's Babel extractor.

    .. Note::

       You only need to use this if you're using Babel's pybabel extract. If
       you're using Puente's extract command, then it does this already and you
       can use the Jinja2 Babel extractor.

    """
    # Must monkeypatch first to fix InternationalizationExtension
    # stomping issues! See docstring for details.
    monkeypatch_i18n()

    return babel_extract(*args, **kwargs)

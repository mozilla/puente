def install_jinja_translations():
    """Install gettext functions into Jingo's Jinja2 environment"""
    from django.utils import translation

    import jingo
    jingo.env.install_gettext_translations(translation, newstyle=True)

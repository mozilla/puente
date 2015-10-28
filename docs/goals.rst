==================
About this project
==================

Why Puente?
===========

Puente is a derivative of `Tower <https://github.com/clouserw/tower>`_, but with
a slightly different scope and a different purpose. Our goals are as follows:

1. Ease translation issues.
2. Correctly support Jinja2 templates.
3. Be as close to vanilla Django as possible.


Ideally, we want to move closer to vanilla Django over time. The best-case
scenario is that no one is using Puente in a couple of years. To get there, we
need to adjust Puente so that it's closer to vanilla Django and also fix things
upstream to meet the needs we have that aren't currently being met.

So, why start a new project instead of continue Tower? Tower is pretty tied to
Jingo and it does a few things I don't want to do anymore. I think this is
enough of a difference that if I took over Tower and then marched it into my
ideal future, users of Tower would get annoyed and I'd hit a lot of friction.
With a library like this where it's pretty small in scope, it seemed way easier
to break with the past, take the interesting parts and start anew.


Current status of phasing Puente out
====================================

We need to do the following before we can end Puente:

1. IN PROGRESS: Jinja2 needs to collapse whitespace in the trans tag

   https://github.com/mitsuhiko/jinja2/issues/504

2. Need to figure out what to do about making gettext output safe for
   Jinja2 templates by default.

3. Puente probably needs a merged makemessages command that does both extract
   and merge and works the way Django's does.

   This should probably be broken up into more steps as we discover differences.

4. Django or django-jinja should grow a proper strings extractor for Jinja2.

   Currently, Django can't extract from Jinja2 templates at all and django-jinja
   tweaks some regexps so that Django's makemessages can "parse' Jinja2
   templates to extract strings. This method isn't great especially if you add
   Jinja2 tags or modify the trans tag or tweak the gettext function.


What's different between Tower and Puente?
==========================================

1. Tower defaults to ``messages.po/pot``, but Puente defaults to ``django.po/pot``.

   FIXME: See if Puente can do messages.po and multiple .po files. Probably
   can't because we nixed all the activation code. Given that, we might
   want to nix the domain code, too, so we only allow for ``django.po`` and
   ``javascript.po``?

   Django's ``makemessages`` command creates a ``django.pot`` file and a
   ``javascript.pot`` file, so that's what we support with Puente, too.

   As far as I can tell, this won't be a problem for most situations. However,
   there is one situation where this makes things difficult. If you had parts of
   the site that **need** to be fully translated and other parts that need to be
   translated, but if it's not translated, it's not a big deal, then this
   makes that difficult.

   One thought I had was to adjust extract/merge to support multiple ``.po``
   files, but then write a ``compilemessages`` command that moves all the
   strings into a single file and then compiles them to a ``.mo`` file. That
   allows us to have different ``.po`` files with different translation
   requirements, but compile down to a single ``django.mo`` and
   ``javascript.mo`` files.

2. Tower collapses whitespace for all extracted strings, but Puente only
   collapses whitespace for Jinja2 trans blocks.

   Django has a ``blocktrans`` tag which since Django 1.7 has had a ``trimmed``
   flag indicating that whitespace should be collapsed. Jinja2 has no such
   thing, but I wrote up an issue for it:

   https://github.com/mitsuhiko/jinja2/issues/504

   If that got implemented, then we could drop the tweaks we do to the ``trans``
   block.

   I think it's important to collapse whitespace in trans blocks because they're
   the most susceptible to msgid changes merely because of adjustments to
   indentation of the HTML template. That stinks because translators have to go
   through and fix all the translations.

3. Tower has a bunch of extract code to support msgctxt, but Puente relies on
   Django's pgettext functions and Babel's msgctxt support.

4. Tower required Jingo, but Puente supports Jingo, django-jinja and other
   Jinja2 template environments.

5. Tower only supports Django 1.7 and lower versions and Puente only supports
   Django 1.7+.

6. Tower supports Python 2.6 and 2.7, but Puente supports 2.7.

7. Tower has most of the code in ``__init__.py``, but Puente tries to be easier
   to use.

8. Tower uses nose for tests, but Puente uses py.test.

   This is purely because I stopped using nose on my projects. Generally, I find
   py.test easier to set up and use these days. I don't want to change this
   unless there's a compelling reason. Generally, if you were maintaining the
   project, I'd encourage you to use whichever test framework works best for
   you.

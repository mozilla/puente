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


Why not just use Babel?
=======================

Puente does three nice things:

1. makes it easy to migrate from Tower to something you can use with Django 1.8
2. collapses whitespace in Jinja2 trans blocks
3. pulls bits from Django settings to configure extraction (e.g. Jinja2
   extensions)

If you don't care about any of those things, go use Babel's pybabel command and
Jinja2's i18n extension--don't use Puente.


What's different between Tower and Puente?
==========================================

1. Tower defaults to ``messages`` and ``javascript``, but Puente defaults to
   ``django`` and ``djangojs``.

   Django's ``makemessages`` command supports ``django`` and ``djangojs``
   domains which create ``django.po(t)`` and ``djangojs.po(t)`` files so that's
   what we support with Puente, too.

   As far as I can tell, this won't be a problem for most situations. However,
   there is one situation where this makes things difficult. If you had parts of
   the site that **need** to be fully translated and other parts that need to be
   translated, but if it's not translated, it's not a big deal, then this makes
   that difficult.

   That's on the list of things to mull over how to deal with.

2. Tower collapses whitespace for all extracted strings, but Puente only
   collapses whitespace for Jinja2 trans blocks.

   Django has a ``blocktrans`` tag which since Django 1.7 has had a ``trimmed``
   flag indicating that whitespace should be collapsed. Jinja2 has no such
   thing, but I wrote up an issue for it:

   https://github.com/mitsuhiko/jinja2/issues/504

   If that got implemented, then we could drop the tweaks we do to the ``trans``
   block and use vanilla Jinja2 trans block.

   I think it's important to collapse whitespace in trans blocks because they're
   the most susceptible to msgid changes merely because of adjustments to
   indentation of the HTML template. That stinks because translators have to go
   through and fix all the translations.

3. Tower had a bunch of code to support msgctxt in extraction and gettext
   calls, but Puente relies on Django's pgettext functions and Babel's
   msgctxt support and that works super.

4. Tower had its own gettext and ngettext that marked output as safe, but Puente
   drops that because it's unneeded if you're using Jinja2's newstyle gettext
   and autoescape enabled.

5. Tower used translate-toolkit to build the ``.pot`` file, but Puente uses
   Babel for putting together the ``.pot`` file. Thus we don't need
   translate-toolkit anymore.

6. Tower required Jingo, but Puente supports Jingo, django-jinja and other
   Jinja2 template environments.

7. Tower only supports Django 1.7 and lower versions and Puente only supports
   Django 1.7+.

8. Tower supports Python 2.6 and 2.7, but Puente supports 2.7. Hopefully Python
   3 in the near future.

9. Tower has most of the code in ``__init__.py``, but Puente tries to be easier
   to use so you can import it without problems.

10. Tower uses nose for tests, but Puente uses py.test.

    This is purely because I stopped using nose on my projects. Generally, I find
    py.test easier to set up and use these days. I don't want to change this
    unless there's a compelling reason. Generally, if you were maintaining the
    project, I'd encourage you to use whichever test framework works best for
    you.


Current status of phasing Puente out
====================================

The best future for Puente is that it gets phased out because it's not needed
anymore.

We need to do the following before we can end Puente:

1. IN PROGRESS: Jinja2 needs to collapse whitespace in the trans tag

   https://github.com/mitsuhiko/jinja2/issues/504

2. Puente's extract command should work more like Babel's pybabel extract
   command.

   The way forward is to phase Puente out for pybabel. In order to make that
   work well, we should mimic pybabel's extract command more closely.

   This should probably be broken up into more steps as we discover differences.

3. Ditch Puente's merge for pybabel's update?

4. Need a nice way to use Django settings for pybabel configuration. For
   example, I'd rather not have to define the list of Jinja2 extensions to use
   in two places.

5. Is there anything else?


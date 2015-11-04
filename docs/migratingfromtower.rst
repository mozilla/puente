====================
Migrating from Tower
====================

Tower and Puente have some differences. If you're using Tower, then you'll need
to do something like the following to switch to Puente.

1. Upgrade to Python 2.7.

   Puente doesn't support Python 2.6, so you're going to have to upgrade.

2. Upgrade to Django 1.7.

3. If you're using Jingo, switch to 0.7.1.

4. Switch from ``messages.po(t)`` to ``django.po(t)``.

   Tower let you have many domains and defaulted to ``messages.po(t)``.

   Puente is moving closer to vanilla Django. Django uses ``django.po(t)`` and
   ``djangojs.po(t)``, so Puente does, too.

   * If you just have ``messages.po(t)`` and ``javascript.po(t)``, then rename
     your ``message.po(t)`` to ``django.po(t)`` and ``javascript.po(t)`` to
     ``djangojs.po(t)`` and sync with your translation system (e.g. Verbatim,
     Pontoon, etc).

   * If you have a bunch of domains and you can squash them all into
     ``django.po(t)`` and ``djangojs.po(t)``, then do that.

   * If you have a bunch of domains and can't squash them into ``django.po(t)``
     and ``djangojs.po(t)``, then we should talk--open up an issue.

5. Sync your strings

   Using Tower, extract, merge and sync strings with Verbatim. That way you
   know exactly what changed for the next few steps.

6. Stop using Tower's gettext.

   Switch instances of this:

   .. code-block:: python

      from tower import ugettext as _


   to this:

   .. code-block:: python

      from django.utils.translation import ugettext as _


   You'll encounter two possible issues here:

   1. If you have consecutive sequences of whitespace in your gettext
      strings, then the msgids will change.

      For example:

      .. code-block:: python

         from tower import ugettext as _
         _('knock knock.    who is there?')


      Tower collapses whitespace in all gettext strings, so that turns
      into ``"knock knock. who is there?"``.

      When you switch that to Django's ugettext, then you're using Tower
      for extraction, but Django's ugettext to look up the translation.
      Because Django's ugettext doesn't collapse whitespace, the msgid
      being used to look up the translation will have all the whitespace
      in it which won't match the msgid in the ``.po`` file and thus
      even though the strings are translated, they won't show up as translated
      on the site.

      You'll need to fix that in the string so the resulting code should
      look like this:

      .. code-block:: python

         from django.utils.translation import ugettext as _
         _('knock knock. who is there?')


      That way the msgid generated during extraction is the same as
      the one that's generated when rendering and that's the same as the
      string the translator translated, so everything should work super.

      Definitely check the msgids after doing this to make sure they're
      the same and fix any issues you see.

   2. Tower's gettext and ngettext supported msgctxt as a separate
      argument.

      For example:

      .. code-block:: python

         from tower import ugettext as _
         _('Orange', 'joke response')
         _('Orange', context='joke response')


      You'll need to switch these to the Django pgettext calls:

      .. code-block:: python

         from django import pgettext
         pgettext('joke response', 'Orange')


      [#]_

      Note that the arguments are reversed!

      https://docs.djangoproject.com/en/1.8/ref/utils/#django.utils.translation.pgettext

      If your test suite covers all code paths that have gettext calls,
      then you can run your test suite and it should error out because
      Tower's gettext and ngettext had an extra argument that Django's
      do not.

      .. [#] Orange who? Orange you glad this example was here to lighten
         the mood?


   At the end of this step, you do not want to be using Tower's gettext at
   all and none of your msgids should have changed.

   You can tell whether msgids have changed by running:

   .. code-block:: bash

      ./manage.py extract


   And diffing the results.

7. Switch from Tower to Puente.

   Puente works with Django 1.7 and Jingo 0.7.1. It also works with Django 1.8+
   and django-jinja. It probably works with other Django Jinja2 template
   environments. If not, let us know.

   1. Remove Tower

   2. Add Puente

   3. Make the configuration changes

      Tower configuration probably looks something like this:

      .. code-block:: python

         # in settings.py
         DOMAIN_METHODS = {
             'django': [
                 ('fjord/**.py', 'tower.tools.extract_tower_python'),
                 ('fjord/**.html', 'tower.tools.extract_tower_template'),
             ],
             'djangojs': [
                 ('**.js', 'javascript')
             ]
         }
         STANDALONE_DOMAINS = ['django']


      The equivalent Puente configuration is something like this:

      .. code-block:: python

         # in settings.py
         PUENTE = {
             'BASE_DIR': BASE_DIR,
             'DOMAIN_METHODS': {
                 'django': [
                     ('fjord/**.py', 'python'),
                     ('fjord/**.html', 'jinja2'),
                 ],
                 'djangojs': [
                     ('**.js', 'javascript')
                 ]
             }
         }


      If you have a more complex Tower configuration than that, hop on
      ``#puente`` on ``irc.mozilla.org`` and we'll work it out.

   4. Add the code to install ugettext/ungettext into the Jinja environment.

      Jingo installs gettext/ngettext functions that don't do anything. You
      will need to install Django's gettext/ngettext functions into the
      environment.

      Calling this during webapp bootstrap will fix that:

      .. code-block:: python

         def install_jinja_translations():
             """Install gettext functions into Jingo's Jinja2 environment"""
             from django.utils import translation

             import jingo
             jingo.env.install_gettext_translations(translation, newstyle=True)


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


   At the end of this step, you do not want to be using Tower's gettext stuff at
   all.

7. Fix strings from non-trans-blocks that had whitespace in them in your code.

   Puente only collapses whitespace for ``trans`` blocks--it no longer collapses
   whitespace for all things. Given that, you want to fix your original strings
   so that the msgids don't change which will create extra work for translators.

   After you've done step 5, you can run:

   .. code-block:: bash

     ./manage.py extract

   and see which msgids changed, then go fix those.

   Generally, you want to switch from Tower to Puente with zero msgid changes.

8. Switch from Tower to Puente.

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

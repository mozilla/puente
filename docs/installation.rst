============
Installation
============

Install
=======

Activate your virtual environment, then do:

.. code-block:: bash

  $ pip install puente


Configure
=========

Puente configuration goes in the ``PUENTE`` setting in your Django settings
file. Here's a minimal example::

   PUENTE = {
       'ROOT': BASE_DIR,
       'DOMAIN_METHODS': {
           'django': [
               ('jinja2/*.html', 'puente.extract.extract_jinja2'),
               ('*.py', 'puente.extract.extract_python')
           ]
       }
   }


This sets up string extraction for ``jinja2/*.html`` files using the Jinja2
extractor, ``*.py`` files using the Python extractor and puts all those strings
in ``django.po(t)`` files.


.. py:data:: ROOT

   :type: String
   :default: None
   :required: Yes


   This is the absolute path to the root directory which has ``locale/`` in it.

   For example::

       /home/willkg/
          - fjord/         <-- ROOT
            - .git/
            - locale/
            - fjord/
              - code!!!
            - manage.py


.. py:data:: DOMAIN_METHODS

   :type: Dict of string to list of (string, string) tuples
   :default: None
   :required: Yes


   Dict of domain name to list of (file matcher, extractor) tuples.

   A domain name here is the name that's used to name the ``.pot`` and ``.po``
   files. For example, if the domain was "django", then the resulting files
   would be ``django.pot`` and ``django.po``.

   The file matcher uses ``*`` and ``**`` glob patterns.

   The extractor is the Babel extractor function used to extract the strings
   from files of that type. Puente helpfully centralizes these in the
   ``puente.extract`` module:

   * ``puente.extract.extract_jinja2``: Extracts strings from Jinja2 templates.
   * ``puente.extract.extract_python``: Extracts strings from Python code
     files.

   For example:

   .. code-block:: python

      PUENTE = {
          'DOMAIN_METHODS': {
              'django': [
                  ('jinja2/*.html', 'puente.extract.extract_jinja2'),
                  ('*.py', 'puente.extract.extract_python')
              ]
          }
      }


.. py:data:: KEYWORDS

   :type: List of strings
   :default: Common gettext indicators
   :required: No


   The list of keywords for functions that are gettext-related. This defaults to
   the list Babel has plus ``_lazy``. If you find it doesn't include all the
   keywords you want, then you can override this.

   There's a ``puente.utils.generate_keywords`` function to make it easier to
   get all the defaults plus the ones you want:

   .. code-block:: python

      from puente.utils import generate_keywords

      PUENTE = {
          'KEYWORDS': generate_keywords(['my', 'special', 'keywords']),
      }


.. py:data:: COMMENT_TAGS

   :type: List of strings
   :default: ``['L10n:', 'L10N:', 'l10n:', 'l10N:']``
   :required: No

   The list of prefixes that denote a comment tag intended for the translator.

   For example, if you had code like this:

   .. code-block:: python

      # l10n: This is a menu name.
      menu_name = _('File')


   Then the comment will get extracted as a translator comment.


.. py:data:: JINJA2_CONFIG

   :type: Dict
   :default: Complicated...
   :required: Possibly

   This is the configuration that the extractor uses to build a Jinja2
   environment in which to parse the template. If this doesn't match the
   environment that your Jinja2 templates are executing in, then you could have
   problems.

   It could have the following things in it depending on how you've configured
   your Django Jinja2 template engine:

   * ``autoescape``: ``True`` or ``False``
   * ``newstyle_gettext``: ``True`` or ``False``
   * ``undefined``: the undefined class to use
   * ``extensions`` list of extensions you're using

   .. Note::

      If you're using django-jinja, then Puente will extract this information
      from the first template handler that uses the
      ``django_jinja.backend.Jinja2`` backend. If that works for you, then you
      don't need to set this.

   Example:

   .. code-block:: python

      PUENTE = {
          'JINJA2_CONFIG`: {
              'autoescape': True,
              'newstyle_gettext': True,
              'extensions': [
                  'jinja2.ext.do',
                  'jinja2.ext.loopcontrols',
                  'jinja2.ext.with_',
                  'jinja2.ext.autoescape',
                  'django_jinja.builtins.extensions.CsrfExtension',
                  'django_jinja.builtins.extensions.StaticFilesExtension',
                  'django_jinja.builtins.extensions.DjangoFiltersExtension',
                  'puente.ext.PuenteI18nExtension',
              ]
          }
      }

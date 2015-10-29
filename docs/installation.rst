============
Installation
============

Install
=======

Activate your virtual environment, then do:

.. code-block:: bash

  $ pip install puente

FIXME: This is a lie until we get it into PyPI.


Configure
=========

In ``settings.py`` add Puente to ``INSTALLED_APPS``:

.. code-block:: python

   INSTALLED_APPS = [
       # ...
       'puente',
       # ...
   ]


In ``settings.py`` add ``puente.ext.PuenteI18nExtension`` as an extension
in your Jinja2 template environment configuration. For example, if you were
using django-jinja, then it might look like this:

.. code-block:: python

   TEMPLATES = [
       {
           'BACKEND': 'django_jinja.backend.Jinja2',
           # ...
           'OPTIONS': {
                # ...
                'extensions': [
                    # ...
                    'puente.ext.PuenteI18nExtension',
                    # ...
            ],
            # ...
       }
       # ...
   ]


Puente configuration goes in the ``PUENTE`` setting in your Django settings
file. Here's a minimal example:

.. code-block:: python

   PUENTE = {
       'BASE_DIR': BASE_DIR,
       'DOMAIN_METHODS': {
           'django': [
               ('jinja2/*.html', 'jinja2'),
               ('*.py', 'python'),
           ]
       }
   }

This sets up string extraction for ``jinja2/*.html`` files using the Jinja2
extractor, ``*.py`` files using the Python extractor and puts all those strings
in ``django.po(t)`` files.

Note that ``BASE_DIR`` is the path to the project root. It's in the
``settings.py`` file that is generated when you create a new Django project.


.. py:data:: BASE_DIR

   :type: String
   :default: None
   :required: Yes


   This is the absolute path to the root directory which has ``locale/`` in it.
   In most cases, it's probably fine to set it to ``BASE_DIR`` which is in the
   ``settings.py`` file that Django generates when you create a new project.

   For example::

       /home/willkg/
          - fjord/         <-- BASE_DIR
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

   The only valid domains are ``django`` and ``djangojs``.

   Valid extractors include:

   * ``python`` for Python files (Babel)
   * ``javascript`` for Javascript files (Babel)
   * ``jinja2`` for Jinja2 templates (Jinja2) [#]_
   * ``ignore`` for files to ignore to alleviate difficulties in file matching
     (Babel)

   You can use extractors provided by other libraries, too. You can also use a
   dotted path to the extraction function.

   For example:

   .. code-block:: python

      PUENTE = {
          'DOMAIN_METHODS': {
              'django': [
                  ('jinja2/*.html', 'jinja2'),
                  ('*.py', 'python')
              ],
              'djangojs': [
                  ('**.js', 'javascript'),
              ]
          }
      }


.. py:data:: KEYWORDS

   :type: Dict of keyword to Babel magic
   :default: Common gettext indicators
   :required: No

   Babel has keywords:

   https://github.com/python-babel/babel/blob/5116c167/babel/messages/extract.py#L31

   Puente adds ``'_lazy': None`` to that.

   Babel uses the keywords to know what strings to extract and how to extract
   them.

   There's a ``puente.utils.generate_keywords`` function to make it easier to
   get all the defaults plus the ones you want:

   .. code-block:: python

      from puente.utils import generate_keywords

      PUENTE = {
          'KEYWORDS': generate_keywords({'foo': None})
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

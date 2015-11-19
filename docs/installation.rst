===============
Install and use
===============

Install
=======

Activate your virtual environment, then do:

.. code-block:: bash

  $ pip install puente


**Optional:** If you want to extract strings from Django templates, you will
also need to install django-babel which has an extractor for Django templates:

.. code-block:: bash

   $ pip install django-babel


Configure
=========

In ``settings.py`` add Puente to ``INSTALLED_APPS``:

.. code-block:: python

   INSTALLED_APPS = [
       # ...
       'puente',
       # ...
   ]


In ``settings.py`` add ``puente.ext.i18n`` as an extension in your Jinja2
template environment configuration. For example, if you were using django-jinja,
then it might look like this:

.. code-block:: python

   TEMPLATES = [
       {
           'BACKEND': 'django_jinja.backend.Jinja2',
           # ...
           'OPTIONS': {
                # ...
                'autoescape': True,
                'extensions': [
                    # ...
                    'puente.ext.i18n',
                    # ...
                ],
           },
       }
   ]


Puente configuration goes in the ``PUENTE`` setting in your Django settings
file. Here's a minimal example:

.. code-block:: python

   PUENTE = {
       'BASE_DIR': BASE_DIR,
       'DOMAIN_METHODS': {
           'django': [
               ('**.py', 'python'),
               ('fjord/**/jinja2/**.html', 'jinja2'),
               ('fjord/**/templates/**.html', 'django'),
           ],
           'djangojs': [
               ('**.js', 'javascript'),
           ]
       }
   }


This sets up string extraction for Jinja2 templates using the Jinja2 extractor,
Python files using the Python extractor, and Django templates using the Django
extractor [#]_ and puts all those strings in ``django.pot`` files.

.. [#] You need to install django-babel for the Django extractor for it to be
   available.

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
   * ``ignore`` for files to ignore to alleviate difficulties in file matching
     (Babel)
   * ``jinja2`` for Jinja2 templates (Jinja2)
   * ``django`` for django templates (django-babel) [#]_

   .. [#] You need to install django-babel for the Django extractor for it to be
      available.

   You can use extractors provided by other libraries, too. You can also write
   your own extractors and use a dotted path to the extraction function.

   Example of ``DOMAIN_METHODS``:

   .. code-block:: python

      PUENTE = {
          'DOMAIN_METHODS': {
              'django': [
                  ('fjord/**/jinja2/**.html', 'jinja2'),
                  ('**.py', 'python')
                  ('fjord/**/templates/**.html', 'django'),
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
   :default: ``['Translators:', 'L10n:', 'L10N:', 'l10n:', 'l10N:']``
   :required: No

   The list of prefixes that denote a comment tag intended for the translator.

   For example, if you had code like this:

   .. code-block:: python

      # l10n: This is a menu name.
      menu_name = _('File')


   Then the comment will get extracted as a translator comment.

   .. Note::

      Django project uses "Translators:", so if you use that, you're closer
      to vanilla Django.


.. py:data:: JINJA2_CONFIG

   :type: Dict
   :default: Complicated...
   :required: Possibly

   This has the options to pass to ``babel_extract``.

   http://jinja.pocoo.org/docs/dev/integration/#babel-integration

   **Setting it yourself**

   Generally, you can add syntax-related options that'd you'd pass in to
   build a new Jinja2 Environment:

   http://jinja.pocoo.org/docs/dev/api/#jinja2.Environment

   Additionally, in Jinja2 2.7, they added a ``silent`` option which dictates
   whether the parser fails silently when parsing Jinja2 templates. This
   commonly happens in two scenarios:

   1. The list of extensions passed isn't the complete list.
   2. The HTML file isn't a Jinja2 template.

   For debugging purposes, you definitely want ``silent=False``.

   Example of ``JINJA2_CONFIG``:

   .. code-block:: python

      PUENTE = {
          'JINJA2_CONFIG`: {
              'extensions': [
                  'jinja2.ext.do',
                  'jinja2.ext.loopcontrols',
                  'jinja2.ext.with_',
                  'jinja2.ext.autoescape',
                  'django_jinja.builtins.extensions.CsrfExtension',
                  'django_jinja.builtins.extensions.StaticFilesExtension',
                  'django_jinja.builtins.extensions.DjangoFiltersExtension',
                  'puente.ext.i18n',
              ]
          }
      }

   **Having Puente figure it out for you**

   If you're using Jingo or django-jinja, then Puente will try to extract the
   list of extensions from the relevant settings. If that works for you, then
   you don't need to set this.

   If Puente is figuring it out, it will automatically add silent=False.

   For example, if you're using django-jinja with these settings:

   .. code-block:: python

      TEMPLATES = [
          {
              'BACKEND': 'django_jinja.backend.Jinja2',
              # ...
              'OPTIONS': {
                   # ...
                   'extensions': [
                       # ...
                       'puente.ext.i18n',
                       # ...
                   ],
              }
          }
      ]

   Then Puente will build something like this:

   .. code-block:: python

      PUENTE = {
         # ...
         'JINJA_CONFIG': {
            'extensions': [
                # ...
                'puente.ext.i18n',
                # ...
            ],
            'silent': 'False'
         }
      }


.. py:data:: PROJECT

   :type: String
   :default: "PROJECT"
   :required: No

   The name of this project. This goes in the ``.pot`` and ``.po`` files and
   could help translators know which project this file that they're translating
   belongs to.

.. py:data:: VERSION

   :type: String
   :default: "1.0"
   :required: No

   The version of this project. This goes in the ``.pot`` and ``.po`` files and
   could help translators know which version of the project this file that
   they're translating belongs to.

.. py:data:: MSGID_BUGS_ADDRESS

   :type: String
   :default: ""
   :required: No

   The email address or url to send bugs related to msgids to. Without this, it's
   hard for a translator to know how to report issues back. If they have this,
   then reporting issues is much easier.

   You want good strings, so this is a good thing to set.

   For example:

   .. code-block:: python

      PUENTE = {
          # ...
          'MSGID_BUGS_ADDRESS': 'https://bugzilla.mozilla.org/enter_bug.cgi?project=Input'
      }


Extract and merge usage
=======================

Message extraction
------------------

After you've configured Puente, you can extract messages like this:

.. code-block:: bash

   $ ./manage.py extract


This will extract all the strings specified by the ``DOMAIN_METHODS``
setting and put them into a ``<domain>.pot`` file.


Message merge
-------------

After you've extracted messages, you'll want to merge new messages into
new or existing locale-specific ``.po`` files. You can merge messages
like this:

.. code-block:: bash

   $ ./manage.py merge

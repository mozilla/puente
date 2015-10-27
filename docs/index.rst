======
puente
======

:Version:       |release|
:Code:          https://github.com/willkg/puente
:License:       BSD; see LICENSE file
:Issues:        https://github.com/willkg/puente/issues
:Documentation: FIXME
:IRC:           #puente on irc.mozilla.org


Puente is a Python library that handles l10n things for Django projects
using Jinja2 templates.

* Babel Python message extractor
* Babel Jinja2 message extractor
* merge command that builds locale directories as needed
* code to collapse whitespace for Jinja2's trans block
* code to mark all gettext output as safe in templates

This is derived from `Tower <https://github.com/clouserw/tower>`_ but
heavily changed to work with Django 1.8 and no longer requires Jinjgo.

FIXME:


Quick start
===========

FIXME: Continue this


User's Guide
============

.. toctree::
   :maxdepth: 2

   readme
   installation
   usage
   migratingfromtower
   authors
   history


Maintainer's Guide
==================

.. toctree::
   :maxdepth: 2

   contributing
   goals


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


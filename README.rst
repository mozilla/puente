======
puente
======

**This is an experiment. Don't use this, yet.**

Puente is a Python library that handles l10n things for Django projects
using Jinja2 templates.

* extract command to extract strings from your project and shove them into a
  ``.pot`` file
* merge command that merges new strings from a ``.pot`` file into locale ``.po``
  files
* Babel Python message extractor
* Babel Jinja2 message extractor
* code to collapse whitespace for Jinja2's trans block
* code to mark all gettext output as safe in templates

This is derived from `Tower <https://github.com/clouserw/tower>`_ but
heavily changed to no longer require Jingo and also support django-jingo
and Django 1.8+.

FIXME:

:Code:          https://github.com/willkg/puente/
:Issues:        https://github.com/willkg/puente/issues
:License:       BSD 3-clause; See LICENSE
:Contributors:  See AUTHORS.rst
:Documentation: https://puente.readthedocs.org/en/latest/
:IRC:           #puente on irc.mozilla.org


Install
=======

From PyPI
---------

Run::

    $ pip install puente

FIXME: Doesn't work until we post it to PyPI.


For hacking
-----------

Run::

    $ git clone https://github.com/willkg/puente
    # Create a virtualenvironment
    $ pip install -r requirements-dev.txt


Usage
=====

See documentation for configuration and usage.

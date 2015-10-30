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
* code to collapse whitespace for Jinja2's trans block
* code to mark all gettext output as safe in templates
* driven from Django settings
* solid documentation

This is derived from `Tower <https://github.com/clouserw/tower>`_, but heavily
changed.

:Code:          https://github.com/mozilla/puente/
:Issues:        https://github.com/mozilla/puente/issues
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


For hacking
-----------

Run::

    # Clone the repository
    $ git clone https://github.com/mozilla/puente

    # Create a virtualenvironment
    ...

    # Install Puente and dev requirements
    $ pip install -r requirements-dev.txt


Usage
=====

See documentation for configuration and usage.

======
puente
======

**Note (2022-05-11): This project is no longer maintained.**

.. image:: puente_logo.jpg

Puente is a Python library that handles l10n things for Django projects
using Jinja2 templates.

* extract command to extract strings from your project and shove them into a
  ``.pot`` file
* merge command that merges new strings from a ``.pot`` file into locale ``.po``
  files
* code to collapse whitespace for Jinja2's trans block
* add pgettext and npgettext to template environment and they correctly
  escape things and work the same way as Jinja2's newstyle gettext
* configured using Django settings
* solid documentation
* solid tests

This is derived from `Tower <https://github.com/clouserw/tower>`_, but heavily
changed.

This project is lightly maintained, and the goal is to phase it out, replacing
it with
`standard Django <https://docs.djangoproject.com/en/2.2/topics/i18n/translation/>`_
for most cases, and 
`Babel <http://babel.pocoo.org/en/latest/>`_ for more complex cases. For more
information, see the issues and the
`current status of phasing Puente out <https://puente.readthedocs.io/en/latest/goals.html#current-status-of-phasing-puente-out>`_.


:Code:          https://github.com/mozilla/puente/
:Issues:        No longer maintained.
:License:       BSD 3-clause; See LICENSE
:Contributors:  See AUTHORS.rst
:Documentation: https://puente.readthedocs.io/


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

See `documentation <https://puente.readthedocs.io/>` for configuration and usage.

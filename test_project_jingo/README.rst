======
README
======

This is a test project for Django 1.7 + Jingo + Puente integration. This
isn't the only way to get these things to work together. It provides us
a test project to verify things are working correctly.


Interesting things
==================

The settings.py file is interesting.

Also, the jingosetup function needs to be called. This installs ugettext and
ungettext into the Jinja2 environment which Jingo doesn't otherwise do for you.


Cleaning the project
====================

Run::

    make clean


This removes artifacts.


Extracting and merging strings
==============================

Run::

   make extract


This cleans the project, then runs extract and merge. This creates the
following two files:

* ``locale/templates/LC_MESSAGES/django.pot``
* ``locale/xx/LC_MESSAGES/django.po``


Translating the xx django.po file
=================================

We use dennis to translat the xx django.po file.

Run::

    make translate


.. Note::

   Dennis 0.7 has two bugs that cause this not to work right, so you're going
   to have to edit the ``.po`` file to fix them. Sorry. :(


Compiling the .po file to a .mo file
====================================

Run::

    make compile


OMG! SO MANY STEPS! Do it all!
==============================

Run::

    make all

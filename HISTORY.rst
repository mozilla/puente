.. :changelog:

=======
History
=======

0.5 (March 3rd, 2017)
=====================

* Drop support for Django 1.7 and Jingo
* Add support for Python 3.5 and 3.6
* Add support for Django 1.9, 1.10 and 1.11b1 (#59) (Thank you, Thor K. H!)


0.4.1 (December 10th, 2015)
===========================

* Add all the Django keywords for extraction (#53)


0.4 (November 20th, 2015)
=========================

* Implement pgettext and npgettext (#45)
* Remove undocumented STANDALONE_DOMAINS setting and fix extract/merge code (#44)
* Add ngettext tests
* Rework gettext code, clarify documentation and add tests (#42)
* Project infrastructure fixes


0.3 (November 5th, 2015)
========================

* add "Translators:" to the translator prefix list (#34)
* make ``puente.ext.i18n`` be an alias for ``puente.ext.PuenteI18nExtension``
* fix the gettext alias to be moar korrect (#35)
* fix the jingo-related docs in regards to extensions (#35)
* lots of changes to the Migrating from Tower document
* fleshed out ``test_project_jingo`` so we can use it for development
* fixed merge to handle ``LANGUAGES`` setting correctly
* first pass on Python 3.4 support (pretty sure it works) (#15)
* logo (#37)


0.2 (October 30th, 2015)
========================

* fix requirements
* remove mention of elasticutils in release process
* fix meta information regarding python 3--we don't support that, yet


0.1 (October 30th, 2015)
========================

Initial writing. Everything has changed!

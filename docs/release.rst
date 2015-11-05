===============
Release process
===============

1. Checkout master tip.

2. Update version numbers in ``puente/__init__.py``.

   1. Set ``__version__`` to something like ``0.4``.
   2. Set ``__releasedate__`` to something like ``20120731``.

3. Update ``AUTHORS.rst``, ``HISTORY.rst``, ``MANIFEST.in``.

   Make sure to set the date for the release in ``HISTORY.rst``.

   Update requirements in ``setup.py``.

4. Verify correctness.

   1. Run tests.
   2. Build docs.
   3. Verify everything works.

5. Tag the release::

       $ git tag -a v0.1

   Copy the details from ``HISTORY.rst`` into the tag comment.

6. Push everything::

       $ git push --tags official master

7. Update PyPI::

       $ rm -rf dist/*
       $ python setup.py sdist bdist_wheel
       $ twine upload dist/*

8. Update topic in ``#puente``, blog post, twitter, etc.

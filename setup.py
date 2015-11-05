#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
from setuptools import setup, find_packages


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')


def get_version():
    VERSIONFILE = os.path.join('puente', '__init__.py')
    VSRE = r"""^__version__ = ['"]([^'"]*)['"]"""
    version_file = open(VERSIONFILE, 'rt').read()
    return re.search(VSRE, version_file, re.M).group(1)


setup(
    name='puente',
    version=get_version(),
    description='Strings extraction and other tools',
    long_description=readme + '\n\n' + history,
    author='Will Kahn-Greene',
    author_email='willkg@mozilla.com',
    url='https://github.com/mozilla/puente',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'babel>=2.1.1',
        'jinja2>=2.7',
        'django>=1.7'
    ],
    license="BSD",
    zip_safe=True,
    keywords='',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
    ],
    test_suite='tests',
    entry_points="""
    [babel.extractors]
    puente_jinja2 = puente.extract:extract_from_jinja2
    """
)

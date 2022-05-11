#!/usr/bin/env python

import os
import re
from setuptools import setup, find_packages


readme = open("README.rst").read()
history = open("HISTORY.rst").read().replace(".. :changelog:", "")


def get_version():
    VERSIONFILE = os.path.join("puente", "__init__.py")
    VSRE = r"""^__version__ = [""]([^""]*)[""]"""
    version_file = open(VERSIONFILE, "rt").read()
    return re.search(VSRE, version_file, re.M).group(1)


setup(
    name="puente",
    version=get_version(),
    description="Strings extraction and other tools -- UNMAINTAINED",
    long_description=readme + "\n\n" + history,
    author="Will Kahn-Greene",
    author_email="willkg@mozilla.com",
    url="https://github.com/mozilla/puente",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Babel>=2.1.1",
        "Jinja2>=2.7",
        "markupsafe",
        "Django>=3.2.0,<4.0.0",
    ],
    license="BSD",
    zip_safe=True,
    keywords="",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    test_suite="tests",
    entry_points="""
    [babel.extractors]
    puente_jinja2 = puente.extract:extract_from_jinja2
    """,
)

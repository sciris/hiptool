#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from setuptools import setup, find_packages

with open("hiptool/version.py", "r") as f:
    version_file = {}
    exec(f.read(), version_file)
    version = version_file["version"]

try:
    from pypandoc import convert
except ImportError:
    import io
    def convert(filename, fmt):
        with io.open(filename, encoding='utf-8') as fd:
            return fd.read()

CLASSIFIERS = [
    'Environment :: Console',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: GPLv3',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Development Status :: 3 - Alpha',
    'Programming Language :: Python :: 2.7',
]

setup(
    name='hiptool',
    version=version,
    author='Cliff Kerr, George Chadderdon',
    author_email='info@hiptool.org',
    description='Health Interventions Prioritization Tool',
    url='http://github.com/sciris/hiptool',
    keywords=['prioritization', 'health services', 'UHC'],
    platforms=['OS Independent'],
    classifiers=CLASSIFIERS,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'scirisweb',
        'matplotlib>=1.4.2',
        'numpy>=1.10.1',
    ],
)

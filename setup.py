#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ast
import re
import uuid

from setuptools import setup
from setuptools.command.test import test as TestCommand
from pip.req import parse_requirements


_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('uhdl/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
    f.read().decode('utf-8')).group(1)))


readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')


reqs = []
links = []
for r in parse_requirements('requirements.txt', session=uuid.uuid1()):
    reqs.append(str(r.req))
    if r.url:
        links.append(str(r.url))


setup(
    name='uhdl',
    version=version,
    description='Python Hardware Description for Humans.',
    long_description=readme + '\n\n' + history,
    author='Keerthan Jaic',
    author_email='jckeerthan@gmail.com',
    url='https://github.com/jck/uhdl',
    packages=[
        'uhdl',
        'uhdl.backends'
    ],
    package_dir={'uhdl': 'uhdl'},
    entry_points={
        'console_scripts': [
            'uhdl = uhdl.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=reqs,
    dependency_links=links,
    license="BSD",
    zip_safe=False,
    keywords='uhdl',
    classifiers=[
        'Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)'
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
)

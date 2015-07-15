#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ast
import re

from setuptools import setup


_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('uhdl/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))


readme = open('README.md').read()

tests_require = ['pytest', 'hypothesis']

setup(
    name='uhdl',
    version=version,
    description='Python Hardware Description for Humans.',
    long_description=readme,
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
            'uhdl = uhdl.cli:cli'
        ]
    },
    include_package_data=True,
    install_requires=[
        'myhdl>=0.9.0',
        'click',
        'wrapt',
    ],
    tests_require=tests_require,
    extras_require = {'test': tests_require},
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
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
    ],
)

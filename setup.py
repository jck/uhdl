#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from setuptools.command.test import test as TestCommand

#from uhdl import __version__
__version__ = '0.0.9'

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')
#requires = ['myhdl', 'clint', 'docopt', 'decorator']
requires = []

setup(
    name='uhdl',
    version=__version__,
    description='Python Hardware Description for Humans.',
    long_description=readme + '\n\n' + history,
    author='Keerthan Jaic',
    author_email='jckeerthan@gmail.com',
    url='https://github.com/jck/uhdl',
    packages=[
        'uhdl',
    ],
    package_dir={'uhdl': 'uhdl'},
    entry_points={
        'console_scripts': [
            'uhdl = uhdl.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requires,
    license="BSD",
    zip_safe=False,
    keywords='uhdl',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    tests_require=['pytest'],
    cmdclass={'test': PyTest},
)

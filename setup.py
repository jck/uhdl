#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand
from pip.req import parse_requirements


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


def get_version():
    for line in open('uhdl/__init__.py'):
        if line.startswith('__version__'):
            for quote in ('"', "'"):
                if quote in line:
                    return line.split(quote)[1]


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


#tmp fix for pip versions below 1.4
class options(object):
    def __getattr__(self, attr):
        return None

reqs = []
links = []
for r in parse_requirements('requirements.txt', options=options()):
    reqs.append(str(r.req))
    if r.url:
        links.append(str(r.url))


setup(
    name='uhdl',
    version=get_version(),
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
    tests_require=['pytest'],
    cmdclass={'test': PyTest},
)

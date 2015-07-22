from setuptools import setup


reqs = [
    'myhdl>=0.9.0',
    'click',
    'wrapt'
]
test_reqs = ['pytest', 'hypothesis']

requires = {
    'setup_requires': ['setuptools_scm'],
    'install_requires': reqs,
    'tests_require': test_reqs,
    'extras_require': {
        'testing': test_reqs,
    }
}

setup(
    name='uhdl',
    use_scm_version=True,
    description='Python Hardware Description for Humans.',
    long_description=open('README.md').read(),
    url='https://github.com/jck/uhdl',
    author='Keerthan Jaic',
    author_email='jckeerthan@gmail.com',
    license="BSD",
    packages=['uhdl'],
    entry_points={
        'console_scripts': [
            'uhdl = uhdl.cli:cli'
        ]
    },
    zip_safe=False,
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
    keywords='myhdl uhdl',
    **requires
)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

import os
from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

# with open('HISTORY.rst') as history_file:
#     history = history_file.read()

def get_version():
    _globals = {}
    with open(os.path.join("fast_curator", "version.py")) as version_file:
        exec(version_file.read(), _globals)
    return _globals["__version__"]

requirements = ['pyyaml', 'six', 'uproot>=4.0.7', 'uproot3']
repositories = []

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', 'flake8', 'pytest-cov', 'xrootd']

setup(
    author="F.A.S.T",
    author_email='fast-hep@cern.ch',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="F.A.S.T. package for describing datasets",
    entry_points={
        'console_scripts': [
            'fast_curator=fast_curator.__main__:main_write',
            'fast_curator_check=fast_curator.__main__:main_check',
        ],
    },
    install_requires=requirements,
    dependency_links=repositories,
    license="Apache Software License 2.0",
    long_description=readme,  # + '\n\n' + history,
    include_package_data=True,
    keywords=['ROOT', 'analysis', 'particle physics', 'HEP', 'F.A.S.T'],
    name='fast-curator',
    packages=find_packages(include=['fast_curator*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/FAST-HEP/fast-curator',
    version=get_version(),
    zip_safe=True,
)

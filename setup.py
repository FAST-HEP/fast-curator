#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

# with open('HISTORY.rst') as history_file:
#     history = history_file.read()

requirements = ['pyyaml', 'six', 'uproot']
repositories = []

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', 'flake8', 'pytest-cov']

setup(
    author="F.A.S.T",
    author_email='fast-hep@cern.ch',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="F.A.S.T. package for describing datasets",
    entry_points={
        'console_scripts': [
            'fast_curator=fast_curator.__main__:main',
        ],
    },
    install_requires=requirements,
    extras_require={'ROOT':  ["rootpy"],
                    },
    dependency_links=repositories,
    license="Apache Software License 2.0",
    long_description=readme,  # + '\n\n' + history,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords=['ROOT', 'analysis', 'particle physics', 'HEP', 'F.A.S.T'],
    name='fast-curator',
    packages=find_packages(include=['fast_curator']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://gitlab.cern.ch/fast-hep/public/fast-curator',
    version='0.1.5',
    zip_safe=True,
)

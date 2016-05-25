#!/usr/bin/env python
import os
import re

from setuptools import setup, find_packages


version = re.compile(r'VERSION\s*=\s*\((.*?)\)')


def get_package_version():
    "returns package version without importing it"
    base = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(base, "teststar/__init__.py")) as initf:
        for line in initf:
            m = version.match(line.strip())
            if not m:
                continue
            return ".".join(m.groups()[0].split(", "))


classes = """
    Development Status :: 4 - Beta
    Intended Audience :: Developers
    License :: OSI Approved :: BSD License
    Topic :: System :: Distributed Computing
    Programming Language :: Python
    Programming Language :: Python :: 2
    Programming Language :: Python :: 2.6
    Programming Language :: Python :: 2.7
    Programming Language :: Python :: Implementation :: CPython
    Operating System :: OS Independent
"""
classifiers = [s.strip() for s in classes.split('\n') if s]


setup(
    name='teststar',
    version=get_package_version(),
    description='Celery TestStar',
    long_description=open('README.rst').read(),
    author='Michael',
    author_email='donzeno23@yahoo.com',
    url='https://github.com/mdaloia/teststar',
    license='BSD',
    classifiers=classifiers,
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=['celery', 'tornado', 'requests', 'redis'],
    package_data={'teststar': ['templates/*', 'static/**/*']},
    entry_points={
        'console_scripts': [
            'teststar = teststar.__main__:main',
        ],
        'celery.commands': [
            'teststar = teststar.command:TestStarCommand',
        ],
    },
)

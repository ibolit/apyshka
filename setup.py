#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

version = "0.0.0"

requirements = [
    "requests>2.10",
]

setup(
    name='apyshka',
    version=version,
    description=(
        'A library for writing wrappers for http calls.'
    ),
    long_description="",
    author='Timofey Danshin',
    author_email='t.danshin@gmail.com',
    url='https://github.com/ibolit/apyshka',
    packages=[
        'apyshka',
    ],
    python_requires='>=3.4',
    install_requires=requirements,
    license='BSD',
    zip_safe=False,
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development',
    ],
    keywords=(),
)

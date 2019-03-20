#!/usr/bin/env python
from setuptools import setup

setup(
    name='verify',
    version='0.0.1.dev1',
    description='A package to perform verifying NWP',
    url='https://github.com/Clarmy/verify',
    author='Clarmy Lee',
    author_email='liwentao@mail.iap.ac.cn',
    license='GPL-3.0',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Software Development :: Quality Assurance',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='verify NWP',
    packages=['bin'],
)

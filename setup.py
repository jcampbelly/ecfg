#!/usr/bin/env python

from distutils.core import setup

with open('LICENSE.md') as f:
    license = f.read()

setup(
    name='ecfg',
    version='0.1.0',
    license=license,
    description='Enlightenment config parser',
    author='Jimmy Campbell',
    author_email='jcampbelly@gmail.com',
    url='https://github.com/jcampbelly/ecfg',
    packages=['ecfg'],
    entry_points=['ecfg:main'],
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'License :: OSI Approved :: MIT License',
        'Topic :: Desktop Environment :: Window Managers :: Enlightenment',
        'Topic :: Software Development :: User Interfaces'
    )
)

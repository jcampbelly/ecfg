#!/usr/bin/env python
# https://pythonhosted.org/setuptools/setuptools.html

from setuptools import setup

with open('LICENSE') as f:
    license = f.read()

setup(
    name='ecfg',
    version='0.1.0',
    license=license,
    description='Enlightenment config parser',
    author='Jimmy Campbell',
    author_email='jcampbelly@gmail.com',
    url='https://github.com/jcampbelly/ecfg',
    install_requires=[
        'pyparsing>=2.0.3'
    ],
    tests_require=[
        'nose==1.3.7',
        'coverage==3.7.1',
        'flake8==2.4.1',
        'mock==1.3.0'
    ],
    test_suite='nose.collector',
    packages=['ecfg'],
    entry_points={'console_scripts': ['ecfg = ecfg.cli:main']},
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

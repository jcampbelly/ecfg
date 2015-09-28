#!/usr/bin/env python
# https://pythonhosted.org/setuptools/setuptools.html

from setuptools import setup

with open('LICENSE') as f:
    license = f.read()

with open('requirements.txt') as f:
    requirements = f.readlines()

# NOTE: It may be necessary to `pip install pbr` for `setup.py test` to work
with open('test_requirements.txt') as f:
    test_requirements = f.readlines()

setup(
    name='ecfg',
    version='0.1.0',
    license=license,
    description='Enlightenment config parser',
    author='Jimmy Campbell',
    author_email='jcampbelly@gmail.com',
    url='https://github.com/jcampbelly/ecfg',
    install_requires=requirements,
    tests_require=test_requirements,
    test_suite='nose.collector',
    packages=['ecfg'],
    entry_points={'console_scripts': ['ecfg = ecfg.cli:main']},
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'License :: OSI Approved :: MIT License',
        'Topic :: Desktop Environment :: Window Managers :: Enlightenment',
        'Topic :: Software Development :: User Interfaces'
    )
)

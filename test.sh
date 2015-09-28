#!/bin/bash
pkg=ecfg
flake8 $pkg
nosetests --with-coverage --cover-branches --cover-package=$pkg

#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""
    Fabric tasker script for pyCurrentCost
"""

from fabric.api import local


OPTIONS = {
    "PYTHON_FILE": "*.py src/*.py src/*/*.py "
    "tests/*.py tests/*/*.py features/steps/*.py",
    "BIN": "data_generator.py"
}

OPTIONS = {
    "PYTHON_FILE": "*.py src/*.py tests/*.py",
    "BIN": "data_generator.py"
}


def test():
    """
        Launch test.
    """
    local("nosetests --cover-erase --with-coverage --cover-html\
         --cover-min-percentage=90 --cover-package=src")
    local("behave")


def pylint():
    """
        Pylint task
    """
    local("pylint %s" % OPTIONS["PYTHON_FILE"])


def clonedigger():
    """
        Clonedigger task
    """
    local("clonedigger %s" % OPTIONS["PYTHON_FILE"])


def pyflakes():
    """
        Pyflakes task
    """
    local("pyflakes %s" % OPTIONS["PYTHON_FILE"])


def pep8():
    """
        Pep8 task
    """
    local("pep8 %s" % OPTIONS["PYTHON_FILE"])


def lint():
    """
        Verify quality code.
    """
    clonedigger()
    pyflakes()
    pep8()
    pylint()


def deploy():
    """
        Deploy and install new version of this product.
    """
    #validate()
    #package()
    #push()
    #install()


def start():
    """
        Start main file of this project
    """
    local("python %s --configfile tests/config/config2.json\
         --action collect" % OPTIONS["BIN"])

#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""
    Fabric tasker script for pyCurrentCost
"""

from fabric.api import local
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


OPTIONS = {
    "PYTHON_FILE": "*.py src/*.py src/*/*.py "
    "tests/*.py tests/*/*.py features/steps/*.py",
    "BIN": "data_generator.py"
}

OPTIONS = {
    "PYTHON_FILE": "*.py src/*.py tests/*.py",
    "BIN": "data_generator.py"
}

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        validate()

def watch():
    """
        Watch current project and launch validate task for each modification.
    """
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)
    observer.start()

    try:
        print('Currently watching recursively this folder !')
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


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


def validate():
    """
        Validate implementation (test and lint code)
    """
    lint()
    test()


def bundle():
    """
        Freeze dependencies for deployment
    """
    local("pip freeze > REQUIREMENTS.txt")
    local("pip bundle data-generator.pybundle -r REQUIREMENTS.txt")


def deploy():
    """
        Deploy and install new version of this product.
    """
    validate()
    #package()
    #push()
    #install()


def start():
    """
        Start main file of this project
    """
    local("python %s --configfile tests/config/config2.json\
         --action collect" % OPTIONS["BIN"])
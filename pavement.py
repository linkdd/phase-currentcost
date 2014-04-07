#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""
    Paver tasker script for pyCurrentCost.
"""

from paver.easy import options, Bunch, task, needs, sh, path
#from paver.easy import *
from paver.setuputils import setup, find_packages
import sys

VERSION = '0.3.7'

INSTALL_REQS = []

if sys.version_info < (3, 0):
    INSTALL_REQS.append('pyserial >= 2.5')
else:
    INSTALL_REQS.append('pyserial-py3k')

PACKAGE = "currentcost"

setup(
    name="pyCurrentCost",
    version=VERSION,
    description="Python script to collect data from current cost EnviR",
    long_description=open('README.md').read(),
    author="Pierre Leray",
    author_email="pierreleray64@gmail.com",
    url="https://github.com/liogen/pyCurrentCost",
    license='LICENSE',
    packages=find_packages(),
    scripts=["bin/currentcost"],
    install_requires=INSTALL_REQS,
    zip_safe=False,
)

options(
    sphinx=Bunch(
        builddir="build",
        sourcedir="source"
    ),

    bin=PACKAGE,

    test_package="tests",

    clone_file="report/clone/index.html",

    stats_file="report/stats/index.html",

    pylint_file=".pylintrc",

    cover_folder="report/cover",

    files="*.py %s/*.py bin/%s %s/*/*.py tests/*.py features/steps/*.py" % (
        PACKAGE, PACKAGE, PACKAGE),
)


@task
@needs(["html", "distutils.command.sdist"])
def sdist():
    """
        Generate docs and source distribution.
    """
    sh('paver develop')


@task
@needs("paver.doctools.html")
def html():
    """
        Build Paver"s documentation and install it into paver/docs.
    """
    builtdocs = path("docs") / options.sphinx.builddir / "html"
    destdir = path(PACKAGE) / "docs"
    destdir.rmtree()
    builtdocs.move(destdir)


@task
def build():
    """
        Validate implementation.
    """
    validate()
    sdist()


@task
def validate():
    """
        Validate implementation.
    """
    lint()
    test()
    stat()


@task
def test():
    """
        Launch unit test
    """
    sh("nosetests --cover-erase --with-coverage --cover-html\
        --cover-package=%s --cover-min-percentage=90 --cover-html-dir=%s" % (
        PACKAGE, options.cover_folder))
    sh("behave")


@task
def pylint():
    """
        Pylint task
    """
    sh("pylint %s -f html --rcfile=%s > %s" % (
        options.files, options.pylint_file, options.stats_file))


@task
def clonedigger():
    """
        Clonedigger task
    """
    sh("clonedigger %s -o %s" % (
        options.files, options.clone_file))


@task
def pyflakes():
    """
        Pyflakes task
    """
    sh("pyflakes %s" % options.files)


@task
def pep8():
    """
        Pep8 task
    """
    sh("pep8 %s" % options.files)


@task
def lint():
    """
        Verify quality code.
    """
    pyflakes()
    pep8()


@task
def stat():
    """
        Verify quality code.
    """
    clonedigger()
    pylint()


@task
def bundle():
    """
        Freeze dependencies for deployment
    """
    sh("pip freeze > REQUIREMENTS.txt")
    sh("pip bundle data-generator.pybundle -r REQUIREMENTS.txt")


@task
def watch():
    """
        Watch current folder and start code inspection for each change.
    """
    sh("watchmedo shell-command \
        --patterns='*.py;*md;' \
        --recursive \
        --command='clear && paver build' \
        .")

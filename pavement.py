#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""
    Paver tasker script for pyCurrentCost.
"""

from paver.easy import options, Bunch, task, needs, sh, path
#from paver.easy import *
from paver.setuputils import setup

setup(
    name="pyCurrentCost",
    version="0.1.8",
    description="Python script to collect data from current cost EnviR",
    author="Pierre Leray",
    author_email="pierreleray64@gmail.com",
    packages=["currentcost"],
    scripts=['bin/currentcost'],
    install_requires=[],
    zip_safe=False,
)

options(
    sphinx=Bunch(
        builddir="build",
        sourcedir="source"
    ),

    bin="currentcost.py",

    package="currentcost",

    test_package="tests",

    clone_file="report/clone/index.html",

    stats_file="report/stats/index.html",

    cover_folder="report/cover",

    #files="*.py currentcost/*.py currentcost/*/*.py tests/*.py tests/*/*.py"
    #    "features/steps/*.py",

    files="*.py currentcost/*.py tests/*.py",
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
    destdir = path(options.package) / "docs"
    destdir.rmtree()
    builtdocs.move(destdir)


@task
def validate():
    """
        Validate implementation.
    """
    sdist()
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
        options.package, options.cover_folder))
    sh("behave")


@task
def pylint():
    """
        Pylint task
    """
    sh("pylint %s -f html > %s" % (options.files, options.stats_file))


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
        --command='clear && paver validate' \
        .")

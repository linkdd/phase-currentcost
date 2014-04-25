#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""
    Paver tasker script for phase-currentcost.
"""

from paver.easy import options, Bunch, task, needs, sh, path

PACKAGE = "currentcost"

options(
    sphinx=Bunch(
        builddir="build",
        sourcedir="source"
    ),

    bin=PACKAGE,

    test_package="tests",

    clone_file="reports/clone/index.html",

    stats_file="reports/stats/index.html",

    cover_folder="reports/cover",

    pylint_file=".pylintrc",

    files="*.py %s/*.py bin/phase-%s tests/*.py features/steps/*.py" % (
        PACKAGE, PACKAGE),
)


@task
def prepare():
    """Install dependencies in this virtualenv

    """
    sh('pip install pylint pyflakes behave nose clonedigger pep8 sphinx')
    sh('pip install watchdog coverage ipython sphinx_rtd_theme')
    develop()


@task
@needs(["html"])
def upload():
    """
        Upload project on PYPI.
    """
    sh('python setup.py register sdist upload')


@task
def develop():
    """
        Generate docs and source distribution.
    """
#   Install package in development mode
    sh('python setup.py develop')


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
@needs(["develop"])
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
        --cover-package=%s --cover-min-percentage=70 --cover-html-dir=%s" % (
        PACKAGE, options.cover_folder))
    sh("behave --tags=-prod")


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
def watch():
    """
        Watch current folder and start code inspection for each change.
    """
    sh("watchmedo shell-command \
        --patterns='*.py;*md;' \
        --recursive \
        --command='clear && paver build' \
        .")

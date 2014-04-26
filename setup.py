#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

""" Setup.py script """

from setuptools import setup
from setuptools.command.install import install
from shutil import copy
import os

VERSION = "1.0.2"

INSTALL_REQS = ["pyserial >= 2.5", "pika"]

PROJECT = "phase"

PLUGIN = "currentcost"


class CustomInstall(install):  # pylint: disable=W0232
    """Add custom installation after pip install.

    """

    def run(self):
        """Main method

        """
        install.run(self)
        # Custom installation steps here
        folder_path = os.path.join("/opt", PROJECT)
        log_folder_path = os.path.join("/var", "log", PROJECT)
        log_conf_path = os.path.join("logs", "%s-%s.conf" % (PROJECT, PLUGIN))
        udev_folder = os.path.join("/etc", "udev", "rules.d")
        udev_file = os.path.join("udev", "70-currentcost.rules")
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        if not os.path.exists(log_folder_path):
            os.makedirs(log_folder_path)
        copy(log_conf_path, folder_path)
        copy(udev_file, udev_folder)


setup(
    name="%s-%s" % (PROJECT, PLUGIN),
    version=VERSION,
    description="Python script to collect data from current cost EnviR",
    long_description=open('README.rst').read(),
    author="Pierre Leray",
    author_email="pierreleray64@gmail.com",
    url="https://github.com/liogen/%s-%s" % (PROJECT, PLUGIN),
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Operating System :: Unix",
        "Programming Language :: Python :: 2.7",
        "Topic :: Home Automation",
        "License :: OSI Approved :: MIT License",
    ],
    packages=[PLUGIN],
    scripts=["bin/%s-%s" % (PROJECT, PLUGIN)],
    install_requires=INSTALL_REQS,
    zip_safe=False,
    cmdclass={'install': CustomInstall},
)

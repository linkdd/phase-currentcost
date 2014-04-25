""" Setup.py script generated by paver """

from setuptools import setup
from setuptools.command.install import install
from shutil import copy
import os

VERSION = "1.0.0"

INSTALL_REQS = ["pyserial >= 2.5", "pika"]


class CustomInstall(install):  # pylint: disable=W0232
    """Add custom installation after pip install.

    """

    def run(self):
        """Main method

        """
        install.run(self)
        # Custom installation steps here
        folder_path = os.path.join('/opt', 'phase')
        log_folder_path = os.path.join('/var', 'log', 'phase')
        log_conf_path = os.path.join('logs', 'phase-currentcost.conf')
        udev_folder = os.path.join('/etc', 'udev', 'rules.d')
        udev_file = os.path.join('udev', '70-currentcost.rules') 
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        if not os.path.exists(log_folder_path):
            os.makedirs(log_folder_path)
        copy(log_conf_path, folder_path)
        copy(udev_file, udev_folder)


setup(
    name="phase-currentcost",
    version=VERSION,
    description="Python script to collect data from current cost EnviR",
    long_description=open('README.rst').read(),
    author="Pierre Leray",
    author_email="pierreleray64@gmail.com",
    url="https://github.com/liogen/phase-currentcost",
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
    packages=["currentcost"],
    scripts=["bin/phase-currentcost"],
    install_requires=INSTALL_REQS,
    zip_safe=False,
    cmdclass={'install': CustomInstall},
)

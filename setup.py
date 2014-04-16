""" Setup.py script generated by paver """

from setuptools import setup, find_packages

VERSION = "0.9.3"

INSTALL_REQS = ["pyserial >= 2.5", "pika"]

setup(
    name="phase-currentcost",
    version=VERSION,
    description="Python script to collect data from current cost EnviR",
    long_description=open('README.rst').read(),
    author="Pierre Leray",
    author_email="pierreleray64@gmail.com",
    url="https://github.com/liogen/phase-currentcost",
    license='LICENSE',
    packages=find_packages(),
    scripts=["bin/currentcost"],
    install_requires=INSTALL_REQS,
    zip_safe=False,
)

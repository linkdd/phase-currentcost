#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""
    Method that parse argument.
"""

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", type=int,
                    help="socket port to publish to 0MQ")
parser.add_argument("variable_name", help="name of the variable")
parser.add_argument("tty", help="tty port to connect to current cost")
parser.add_argument("-v", "--verbose", help="activate verbose mode",
                    action="store_true")


def argument_parser():
    """
        Method that parse argument,
        return an error in case of missing paramter or
        return argument with their value.
    """
    args = parser.parse_args()
    return args.variable_name, args.port, args.tty, args.verbose

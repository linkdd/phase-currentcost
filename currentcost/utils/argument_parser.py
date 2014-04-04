#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""
    Method that parse argument.
"""

import argparse

PARSER = argparse.ArgumentParser()
PARSER.add_argument("variable_name", help="name of the variable")
PARSER.add_argument("tty", help="tty port to connect to current cost")
PARSER.add_argument("-v", "--verbose", help="activate verbose mode",
                    action="store_true")


def argument_parser():
    """
        Method that parse argument,
        return an error in case of missing paramter or
        return argument with their value.
    """
    args = PARSER.parse_args()
    return args.variable_name, args.tty, args.verbose

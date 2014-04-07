#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""
    Method that parse argument.
"""

import argparse


def argument_parser():
    """
        Method that parse argument,
        return an error in case of missing paramter or
        return argument with their value.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("variable_name", help="name of the variable")
    parser.add_argument("site_name",
                        help="name of the location of the variable")
    parser.add_argument("-t", "--tty-port",
                        help="tty port to connect to current cost")
    parser.add_argument("-r", "--rabbitMQ-credential",
                        help="credential for rabbitMQ. By default, RabbitMQ is\
                        deactivated. To activate it you have to give your \
                        credential. Format: username:password.")
    parser.add_argument("-v", "--verbose", help="activate verbose mode",
                        action="store_true")
    return parser.parse_args()

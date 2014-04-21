#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""Globals and function needs for this project.

.. module:: utils
    :platform: Unix
    :synopsis: This module contains all useful globals and function needed.

.. moduleauthor:: Pierre Leray <pierreleray64@gmail.com>

"""

import argparse
import logging
from datetime import datetime
from xml.etree import ElementTree

# Globals declaration for this project
SUCCESS = "currentcost"
ERROR = "error"
TTY_CONNECTION_PROBLEM = "CurrentCost %s in %s: TTY connection problem: %s \
is unreachable. Retry connection in 5 seconds."
TTY_TRYING_CONNECTION = "CurrentCost %s in %s: Trying to connect to %s."
TTY_CONNECTION_SUCCESS = "CurrentCost %s in %s: Success connection to %s."
TTY_DISCONNECTED = "CurrentCost %s in %s: TTY port %s disconnected."
CURRENTCOST_TIMEOUT = "CurrentCost %s in %s: Reach timeout. Verify \
CurrentCost wire connection or wave range"
CC_INCORRECT_MESSAGE = "CurrentCost %s in %s: Send incorrect \
message => %s."
RABBIT_MQ_CONNECTION_PROBLEM = "Problem trying to connect to RabbitMQ with \
this configuration: username: %s, password: %s, host: %s"
RABBIT_MQ_CREDENTIAL_PROBLEM = "Problem bad RabbitMQ credential with \
this configuration: username: %s, password: %s, host: %s"
CURRENTCOST_UNICODE_ERROR = "Bad message sent from currentcost, invalid ASCII"
# Logger initialization
LOGGER = logging.getLogger("currentcost")


def argument_parser():
    """Method that parse arguments from command line, return an error in
    case of missing parameter or return arguments with their value.

    :returns:  dict -- Dict containing arguments.

    """
#   Get command line arguments
    parser = argparse.ArgumentParser()
#   Define expected arguments
    parser.add_argument("variable_name", help="name of the variable")
    parser.add_argument("site_name",
                        help="name of the location of the variable")
    parser.add_argument("-t", "--tty-port",
                        help="tty port to connect to current cost")
    parser.add_argument("-r", "--rabbitmq-credential",
                        help="credential for rabbitMQ. By default, RabbitMQ is\
                        deactivated. To activate it you have to give your \
                        credential. Format: username:password.")
    parser.add_argument("-v", "--verbose", help="activate verbose mode",
                        action="store_true")
#   Return list of argument passed in command line
    return parser.parse_args()


def init_message(variable_name, site_name, tty_port):
    """Create log message starting current cost.

    :param variable_name: Name of the Variable.
    :type variable_name: str.

    :param site_name: Name of the Site.
    :type site_name: str.

    :param tty_port: TTY port path.
    :type tty_port: str.
    """
#   Create init message
    message = "Starting current cost application\n"
    message += "Current time: %s\n" % datetime.now()
    message += "Variable name: %s\n" % variable_name
    message += "Site name: %s\n" % site_name
    message += "TTY port: %s\n" % tty_port
#   We log this message
    LOGGER.info(message)


def verbose_mode(verbose):
    """Active verbose mode.

    :param verbose: Boolean if true active verbose mode.
    :type variable_name: bool.
    """
#   If verbose mode is activated
    if verbose:
#       Create an handler to console and display log message
        sth = logging.StreamHandler()
        sth.setLevel(logging.INFO)
#       Add this handler to current logger
        LOGGER.addHandler(sth)


def data_validator(data, variable_name, site_name):
    """Analyse data from currentcost and return according TOPIC and MESSAGE.

    :param data: XML string that contain data.
    :type variable_name: str.

    :param variable_name: Name of the Variable.
    :type variable_name: str.

    :param site_name: Name of the Site.
    :type site_name: str.

    :returns:  str -- Topic of the message (error or success) and
    Message containing error description or data sent by CC.
    """
#   Initialization of variable
    topic = ERROR
    message = None
#   If data is empty, that means we reach a Timeout
    if data == "":
        message = CURRENTCOST_TIMEOUT % (variable_name, site_name)
#   Else we retrieve a string
    else:
#       We remove useless end-line and new-line caracteres
        data = data.replace("\n", "").replace("\r", "")
        try:
#           We expect a valid XML
            ElementTree.fromstring(data)
        except ElementTree.ParseError:
            try:
#               If it's not a valid XML, we expected it's a good string
#               and return an error
                message = CC_INCORRECT_MESSAGE % (
                    variable_name,
                    site_name,
                    data)
            except UnicodeDecodeError:
#               If it's not a good string, we send according message
                message = CC_INCORRECT_MESSAGE % (
                    variable_name,
                    site_name,
                    CURRENTCOST_UNICODE_ERROR)
        else:
#           Else, we return our message with according topic
            topic = SUCCESS
            message = data

    return topic, message

#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""
    Method that send message over the network.
"""

# logging is the most used python logger
import logging

LOGGER = logging.getLogger("currentcost")


def send_message(topic, message):
    """
        Method that send a message with a topic.
    """
    print topic
    print message
    return True


def send_error(topic, message):
    """
        Method that send a message with a topic.
    """
    LOGGER.error(message)
    return True

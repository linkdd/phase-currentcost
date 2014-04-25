#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-
# pylint: disable=R0904

"""
    Test file for utils file.
"""

from __future__ import print_function
import unittest
from currentcost.utils import ERROR, CURRENTCOST_TIMEOUT
from currentcost.utils import SUCCESS, CC_INCORRECT_MESSAGE, data_validator
# from currentcost.utils import CURRENTCOST_UNICODE_ERROR
import logging
import logging.config

DEFAULT_LOG_FILE = "logs/log.conf"

logging.config.fileConfig(DEFAULT_LOG_FILE)

VAR_NAME = "TEST_electric_meter"
SITE_NAME = "TEST_liogen_home"
TIMEOUT_DATA = ""
CURRENTCOST_MESSAGE = "<msg><src>CC128-v1.29</src><dsb>00786</dsb>\
<time>00:31:36</time><tmpr>19.3</tmpr><sensor>0</sensor><id>00077</id>\
<type>1</type><ch1><watts>00405</watts></ch1></msg>"
WRONG_UNICODE = "efghjkl"
WRONG_CURRENTCOST_MESSAGE = "<msg><src>ensor>0</sensor><id>00077</id>\
<type>1</type><ch1><watts>00405</watts></ch1></msg>"


class TestUtils(unittest.TestCase):

    """
        All test case for utils file.
    """

    def test_data_parser(self):
        """
            Test add function for generator class.
        """
#       Data parser for valid XML
        topic, message = data_validator(
            CURRENTCOST_MESSAGE,
            VAR_NAME,
            SITE_NAME)
        self.assertEqual(topic, SUCCESS)
        self.assertEqual(message, CURRENTCOST_MESSAGE)

#       Data parser for invalid XML
        topic, message = data_validator(
            WRONG_CURRENTCOST_MESSAGE,
            VAR_NAME,
            SITE_NAME)
        self.assertEqual(topic, ERROR)
        self.assertEqual(message, CC_INCORRECT_MESSAGE % (
            VAR_NAME,
            SITE_NAME,
            WRONG_CURRENTCOST_MESSAGE))

#       Data parser for invalid unicode string
        # (need to find a way to simualte a wrong unicode string)
        # topic, message = data_validator(WRONG_UNICODE, VAR_NAME, SITE_NAME)
        # self.assertEqual(topic, ERROR)
        # self.assertEqual(message, CC_INCORRECT_MESSAGE % (
        #     VAR_NAME,
        #     SITE_NAME,
        #     CURRENTCOST_UNICODE_ERROR))

#       Data parser for CurrentCost timeout
        topic, message = data_validator(TIMEOUT_DATA, VAR_NAME, SITE_NAME)
        self.assertEqual(topic, ERROR)
        self.assertEqual(message, CURRENTCOST_TIMEOUT % (
            VAR_NAME,
            SITE_NAME))

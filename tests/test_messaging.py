#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-
# pylint: disable=R0904

"""
    Test file for messaging method.
"""

import unittest
from currentcost.messaging import send_message, send_error


class TestMessaging(unittest.TestCase):

    """
        All test case for messaging method.
    """

    def test_send_message(self):
        """
            Test add function for generator class.
        """
        self.assertEqual(send_message("re", "er"), True)

    def test_send_error(self):
        """
            Test add function for generator class.
        """
        self.assertEqual(send_error("re", "er"), True)

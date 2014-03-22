#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-
# pylint: disable=R0904

"""
    Test file for messaging method.
"""

import unittest
from src.messaging import sendMessage


class TestMessaging(unittest.TestCase):

    """
        All test case for messaging method.
    """

    def test_send_message(self):
        """
            Test add function for generator class.
        """
        self.assertEqual(sendMessage("re", "er"), True)

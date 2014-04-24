#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-
# pylint: disable=R0904

"""
    Test file for RabbitMQMessager method.
"""

from __future__ import print_function
import unittest
from currentcost.messager import RabbitMQMessager
from io import StringIO
import pika
import logging
import logging.config
from time import tzname
import json

VALID_USERNAME = "admin"
VALID_PASSWORD = "password"
VALID_HOST = "localhost"
INVALID_USERNAME = "EDzadminZE"
INVALID_PASSWORD = "pasZECZCordZE"
INVALID_HOST = "192.168.5.56"
TOPIC = "TEST_RABBIT_MQ_MESSAGER"
MESSAGE = "It works!"
SITE_NAME = "TEST_SITE"
VAR_NAME = "TEST_VAR"
CREDENTIALS = pika.PlainCredentials(VALID_USERNAME, VALID_PASSWORD)
CONNECTION = pika.BlockingConnection(
    pika.ConnectionParameters(host=VALID_HOST, credentials=CREDENTIALS))
DEFAULT_LOG_FILE = "logs/log.conf"

logging.config.fileConfig(DEFAULT_LOG_FILE)


def validate_stdout(username, password, host, self):
    """
        Send a message on stdout and expecting to see it.
    """
    messager = RabbitMQMessager(username, password, host)
    self.assertEqual(messager.channel, None)
    out = StringIO()

    messager.send(TOPIC, MESSAGE, out)
    output = out.getvalue().strip()
    self.assertEqual(output, MESSAGE)

    out2 = StringIO()
    messager.send_message(TOPIC, SITE_NAME, VAR_NAME, MESSAGE, out2)
    output2 = json.loads(out2.getvalue().strip())
    self.assertEqual(output2["message"], MESSAGE)
    self.assertEqual(output2["siteID"], SITE_NAME)
    self.assertEqual(output2["variableID"], VAR_NAME)
    self.assertEqual(output2["dstTimezone"], tzname[1])
    self.assertEqual(output2["nonDstTimezone"], tzname[0])


class TestRabbitMQMessager(unittest.TestCase):

    """
        All test case for messaging method.

        Tests:

        * Test messager without credential:
            => self.channel should be None
            => send method should print on stdout
        * Test message with good credentials:
            => self.channel should be different of None
            => send message should send a message on RabbitMQ
        * Test message with bad credentials:
            => self.channel should be None
            => send method should print on stdout
        * Test message with invalid host:
            => self.channel should be None
            => send method should print on stdout
    """

    def callback(self, channel, method, properties, body):
        """
            Callback called when a new message is available.
        """
        print(method)
        print(properties)
        self.assertEqual(body, MESSAGE)
        channel.close()

    def test_without_credential(self):
        """
            Test add function for generator class.
        """
        validate_stdout(None, None, VALID_HOST, self)

    def test_bad_credential(self):
        """
            Test add function for generator class.
        """
        validate_stdout(INVALID_USERNAME, INVALID_PASSWORD, VALID_HOST, self)

    def test_bad_host(self):
        """
            Test add function for generator class.
        """
        validate_stdout(VALID_USERNAME, VALID_PASSWORD, INVALID_HOST, self)

    def test_good_credential(self):
        """
            Test add function for generator class.
        """
        messager = RabbitMQMessager(VALID_USERNAME, VALID_PASSWORD, VALID_HOST)
        self.assertNotEqual(messager.channel, None)
        messager.send(TOPIC, MESSAGE)
        messager.consume(TOPIC, self.callback)

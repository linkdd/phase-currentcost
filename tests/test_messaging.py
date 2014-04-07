#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-
# pylint: disable=R0904

"""
    Test file for messaging method.
"""

import unittest
from currentcost.rabbitmq_messager import RabbitMQMessager
from io import StringIO
import pika
import logging
import logging.config

VALID_USERNAME = "admin"
VALID_PASSWORD = "password"
VALID_HOST = "localhost"
INVALID_USERNAME = "EDzadminZE"
INVALID_PASSWORD = "pasZECZCordZE"
INVALID_HOST = "192.168.5.56"
TOPIC = "TEST_RABBIT_MQ_MESSAGER"
MESSAGE = u"It works!"
CREDENTIALS = pika.PlainCredentials(VALID_USERNAME, VALID_PASSWORD)
CONNECTION = pika.BlockingConnection(
    pika.ConnectionParameters(host=VALID_HOST, credentials=CREDENTIALS))
DEFAULT_LOG_FILE = "logs/log.conf"

logging.config.fileConfig(DEFAULT_LOG_FILE)


class TestMessaging(unittest.TestCase):

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
        self.assertEqual(body, MESSAGE)
        CONNECTION.close()

    def test_without_credential(self):
        """
            Test add function for generator class.
        """
        messager = RabbitMQMessager(None, None, VALID_HOST)
        self.assertEqual(messager.channel, None)
        out = StringIO()
        messager.send(TOPIC, MESSAGE, out)
        output = out.getvalue().strip()
        self.assertEqual(output, MESSAGE)

    def test_bad_credential(self):
        """
            Test add function for generator class.
        """
        messager = RabbitMQMessager(
            INVALID_USERNAME,
            INVALID_PASSWORD,
            VALID_HOST)
        self.assertEqual(messager.channel, None)
        out = StringIO()
        messager.send(TOPIC, MESSAGE, out)
        output = out.getvalue().strip()
        self.assertEqual(output, MESSAGE)

    def test_bad_host(self):
        """
            Test add function for generator class.
        """
        messager = RabbitMQMessager(
            VALID_USERNAME,
            VALID_PASSWORD,
            INVALID_HOST)
        self.assertEqual(messager.channel, None)
        out = StringIO()
        messager.send(TOPIC, MESSAGE, out)
        output = out.getvalue().strip()
        self.assertEqual(output, MESSAGE)

    def test_good_credential(self):
        """
            Test add function for generator class.
        """
        messager = RabbitMQMessager(VALID_USERNAME, VALID_PASSWORD, VALID_HOST)
        self.assertNotEqual(messager.channel, None)
        messager.send(TOPIC, MESSAGE)
        channel = CONNECTION.channel()
        channel.queue_declare(queue=TOPIC)
        try:
            channel.basic_consume(self.callback, queue=TOPIC, no_ack=True)
            channel.start_consuming()
        except pika.exceptions.ConnectionClosed:
            pass

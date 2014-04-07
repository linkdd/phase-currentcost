#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""
    Method that send message over the network.
"""

import logging
import pika
import sys
from currentcost.utils import error_utils


class RabbitMQMessager(object):

    """
        This class send message to RabbitMQ or in stdout following user choice.
    """

    def __init__(self, username, password, host):
        """
            Constructor.

            Init RabbitMQ.
        """
        self.logger = logging.getLogger("currentcost.pika")
        self.channel = None

        if username is not None and password is not None:
            try:
                self.connection = pika.BlockingConnection(
                    pika.ConnectionParameters(
                        host=host,
                        credentials=pika.PlainCredentials(username, password)))
                self.channel = self.connection.channel()
            except pika.exceptions.ConnectionClosed:
                # Credential error
                self.logger.error(error_utils.RABBIT_MQ_CREDENTIAL_PROBLEM % (
                    username, password, host))
            except pika.exceptions.AMQPConnectionError:
                # Host error
                self.logger.error(error_utils.RABBIT_MQ_CONNECTION_PROBLEM % (
                    username, password, host))

    def send(self, topic, message, out=sys.stdout):
        """
            Method that send a message with a topic.
        """
        self.logger.error(message)
        if self.channel is not None:
            self.channel.queue_declare(queue=topic)
            self.channel.basic_publish(
                exchange='', routing_key=topic, body=message)
        else:
#           Print on terminal
            out.write("%s %s" % (message, "\n"))

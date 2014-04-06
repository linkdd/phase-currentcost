#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""
    Method that send message over the network.
"""

from __future__ import print_function
import logging
import pika


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

        if username is not None and password is not None:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=host,
                    credentials=pika.PlainCredentials(username, password)))
            self.channel = self.connection.channel()
        else:
            self.channel = None

    def send(self, topic, message):
        """
            Method that send a message with a topic.
        """
        self.logger.error(message)
        if self.channel is not None:
            self.channel.queue_declare(queue=topic)
            self.channel.basic_publish(
                exchange='', routing_key=topic, body=message)
        else:
            print(message)

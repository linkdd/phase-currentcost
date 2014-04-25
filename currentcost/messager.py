#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""Method that send message on RabbitMQ or display it on stdout.

.. moduleauthor:: Pierre Leray <pierreleray64@gmail.com>

"""

import logging
import pika
import sys
from currentcost.utils import RABBIT_MQ_CREDENTIAL_PROBLEM
from currentcost.utils import RABBIT_MQ_CONNECTION_PROBLEM
from time import tzname
from datetime import datetime
import json


class RabbitMQMessager(object):

    """This class send message to RabbitMQ or in stdout following user choice.

    """

    def __init__(self, username, password, host):
        """Constructor.

            :param username: Name of the RabbitMQ user.
            :type username: str.

            :param password: Password of the RabbitMQ user.
            :type password: str.

            :param host: Host target for RabbitMQ.
            :type host: str.
        """
        # Logger and channel initialization
        self.logger = logging.getLogger("currentcost.pika")
        self.channel = None
        # If we have a username and password for RabbitMQ
        if username is not None and password is not None:
            try:
                # We try to connect to RabbitMQ with this credential
                self.connection = pika.BlockingConnection(
                    pika.ConnectionParameters(
                        host=host,
                        credentials=pika.PlainCredentials(username, password)))
                # If our connection was successful we retrieve a channel
                self.channel = self.connection.channel()
            except pika.exceptions.ConnectionClosed:
                # Else if our credential were wrong, we log according message
                error = RABBIT_MQ_CREDENTIAL_PROBLEM % (
                    username,
                    password,
                    host)
                self.logger.error(error)
            except pika.exceptions.AMQPConnectionError:
                # Else if RabbitMQ is not available in this location,
                # we log according message
                error = RABBIT_MQ_CONNECTION_PROBLEM % (
                    username,
                    password,
                    host)
                self.logger.error(error)

    def send(self, topic, message, out=sys.stdout):
        """Method that send a message with a topic.

            :param topic: Channel where to send message (RabbitMQ filter).
            :type topic: str.

            :param message: Message to send to RabbitMQ.
            :type message: str.

            :param out: Stdout redirection in case of test (default: stdout).
            :type out: StringIO.
        """
        # We log message we want to send to keep a trace
        self.logger.error(message)
        # If channel is available
        if self.channel is not None:
            # We send a message on this channel
            self.channel.queue_declare(queue=topic)
            self.channel.basic_publish(
                exchange='', routing_key=topic, body=message)
        else:
            # Else we print it in stdout
            out.write("%s %s" % (unicode(message), "\n"))

    def send_message(self, topic, site_name, var_name, data, out=sys.stdout):
        """Format parameter into json string for phase platform.

            :param topic: Channel where to send message (RabbitMQ filter).
            :type topic: str.

            :param site_name: Name of the site.
            :type site_name: str.

            :param var_name: Variable name.
            :type var_name: str.

            :param data: Data send to send.
            :type data: str.

            :param out: Stdout redirection in case of test (default: stdout).
            :type out: StringIO.
        """
        # We create our phase message
        json_message = {
            'siteID': site_name,
            'variableID': var_name,
            'message': data,
            'date': datetime.utcnow().isoformat('T'),
            'dstTimezone': tzname[1],
            'nonDstTimezone': tzname[0]
        }
        # And we send it using our send method defined previously
        self.send(topic, json.dumps(json_message), out)

    def consume(self, topic, callback):
        """Method that wait for a message on RabbitMQ topics channels.

            :param topic: Channel where to send message (RabbitMQ filter).
            :type topic: str.

            :param callback: Function that compute result of message (async).
            :type callback: Function.
        """
        # We try to connect to our channel and wait for a message
        try:
            self.channel.queue_declare(queue=topic)
            self.channel.basic_consume(callback, queue=topic, no_ack=True)
            self.channel.start_consuming()
        except pika.exceptions.ConnectionClosed:
            # If something goes wrong we pass silently
            pass

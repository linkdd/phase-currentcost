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
from time import tzname
from datetime import datetime
import json


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
        self.logger.info(message)
        if self.channel is not None:
            self.channel.queue_declare(queue=topic)
            self.channel.basic_publish(
                exchange='', routing_key=topic, body=message)
        else:
#           Print on terminal
            out.write("%s %s" % (unicode(message), "\n"))

    def send_message(self, topic, site_name, var_name, data, out=sys.stdout):
        """
            Format parameter into json string for phase platform.
        """
        json_message = {
            'siteID': site_name,
            'variableID': var_name,
            'message': data,
            'date': datetime.utcnow().isoformat('T'),
            'dstTimezone': tzname[1],
            'nonDstTimezone': tzname[0]
        }
        # json_encoded = json.dumps(json_message)
        # print json_encoded
        # test = json.loads(json_encoded.decode("utf-8"))
        # print test[u"message"]
        self.send(topic, json.dumps(json_message), out)

    def consume(self, topic, callback):
        """
            Method that wait for a message on RabbitMQ topics channels.
        """
        try:
            self.channel.queue_declare(queue=topic)
            self.channel.basic_consume(callback, queue=topic, no_ack=True)
            self.channel.start_consuming()
        except pika.exceptions.ConnectionClosed:
            pass

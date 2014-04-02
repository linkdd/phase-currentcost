#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""
    Method that send message over the network.
"""

# logging is the most used python logger
import logging
import pika

LOGGER = logging.getLogger("currentcost.pika")

CREDENTIALS = pika.PlainCredentials("admin", "password")
CONNECTION = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', credentials=CREDENTIALS))


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
    channel = CONNECTION.channel()
    channel.queue_declare(queue=topic)
    channel.basic_publish(exchange='', routing_key=topic, body=message)
    CONNECTION.close()

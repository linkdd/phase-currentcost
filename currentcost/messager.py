#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""Method that send message on RabbitMQ or display it on stdout.

.. moduleauthor:: Pierre Leray <pierreleray64@gmail.com>

"""

from dateutil.parser import parse as parse_date
from xml.etree import ElementTree

import logging
import pika
import sys
from currentcost.utils import RABBIT_MQ_CREDENTIAL_PROBLEM
from currentcost.utils import RABBIT_MQ_CONNECTION_PROBLEM
from time import tzname
import datetime
import json


class RabbitMQMessager(object):

    """This class send message to RabbitMQ or in stdout following user choice.

    """

    def __init__(self, rabbitmq_url, config):
        """Constructor.

            :param rabbitmq_url: RabbitMQ address.
            :type rabbitmq_url: basestring

            :param config: Plugin configuration.
            :type config: ConfigParser
        """
        # Logger and channel initialization
        self.logger = logging.getLogger("currentcost.pika")
        self.channel = None

        self.canopsis_mode = config.has_section('canopsis') and config.getboolean('canopsis', 'enabled')
        self.config = config

        # If we have a username and password for RabbitMQ
        if rabbitmq_url is not None:

            try:
                # We try to connect to RabbitMQ with this credential
                self.connection = pika.BlockingConnection(
                    pika.URLParameters(rabbitmq_url))
                # If our connection was successful we retrieve a channel
                self.channel = self.connection.channel()
            except pika.exceptions.ConnectionClosed:
                # Else if our credential were wrong, we log according message
                error = RABBIT_MQ_CREDENTIAL_PROBLEM % rabbitmq_url
                self.logger.error(error)
            except pika.exceptions.AMQPConnectionError:
                # Else if RabbitMQ is not available in this location,
                # we log according message
                error = RABBIT_MQ_CONNECTION_PROBLEM % rabbitmq_url
                self.logger.error(error)

    def build_canopsis_event(self, message):
        """Method that transform message into a Canopsis event.

            :param message: Message to send to RabbitMQ.
            :type message: dict.

            :returns: routing key, body
        """

        event = {
            'connector': self.config.get('canopsis', 'connector'),
            'connector_name': self.config.get('canopsis', 'connector_name'),
            'component': self.config.get('canopsis', 'component'),
            'resource': self.config.get('canopsis', 'resource')
        }

        for key,value in event.iteritems():
            if value.startswith('$'):
                mkey = value[1:]
                event[key] = message[mkey]

        event.update({
            'event_type': 'check',
            'source_type': 'resource',
            'timestamp': int(parse_date(message['date']).strftime('%s')),
            'state': 0,
            'state_type': 1
        })

        # Parse perfdata
        try:
            root = ElementTree.fromstring(message['message'])

        except ElementTree.ParseError:
            event['output'] = message['message']
            event['state'] = 2

        else:
            strtime = root.find('./time').text
            hours, mins, seconds = strtime.split(':')
            seconds = seconds + mins * 60 + hours * 60 * 60

            dsb = int(root.find('./dsb').text)

            event['perf_data_array'] = [{
                'metric': 'uptime',
                'value': datetime.timedelta(days=dsb, seconds=seconds).total_seconds,
                'unit': 's',
                'type': 'GAUGE'
            },{
                'metric': 'temp',
                'value': float(root.find('./tmpr').text),
                'type': 'GAUGE'
            },{
                'metric': 'watts',
                'value': float(root.find('./ch1/watts').text),
                'type': 'GAUGE'
            }]

        rk = '{0}.{1}.{2}.{3}.{4}.{5}'.format(
            event['connector'],
            event['connector_name'],
            event['event_type'],
            event['source_type'],
            event['component'],
            event['resource']
        )

        return rk, json.dumps(event)

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
            if self.canopsis_mode:
                try:
                    msg = json.loads(message)
                    rk, body = self.build_canopsis_event(msg)

                    self.channel.basic_publish(
                        exchange='canopsis.events',
                        routing_key=rk,
                        body=body)

                except ValueError as err:
                    self.logger.error('Impossible to decode message: %s', err)

            else:
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
            'date': datetime.datetime.utcnow().isoformat('T'),
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

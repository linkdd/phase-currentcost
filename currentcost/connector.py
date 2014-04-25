#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""Method that connect to Current Cost and read message from TTY port.

.. moduleauthor:: Pierre Leray <pierreleray64@gmail.com>

"""

import logging
from currentcost.utils import data_validator, TTY_CONNECTION_PROBLEM, ERROR
from currentcost.utils import TTY_CONNECTION_SUCCESS, TTY_DISCONNECTED
import serial
from time import sleep

LOGGER = logging.getLogger("currentcost.currentcost")
BAUDS = 57600
USB_RETRY = 5


class CurrentCostConnector(object):

    """This class connect to current cost through tty port and read data.

    """

    def __init__(self, site_name, variable_name, tty_port, timeout):
        """Constructor.

            :param site_name: Name of the site.
            :type site_name: str.

            :param variable_name: Name of the variable.
            :type variable_name: str.

            :param tty_port: Port to connect to CurrentCost.
            :type tty_port: str.

            :param timeout: Time to reach timeout and send error.
            :type timeout: str.
        """
        # Initialization of class attributes
        self.site_name = site_name
        self.variable_name = variable_name
        self.tty_port = tty_port
        self.timeout = timeout
        self.serial_connection = None

    def readlines(self):
        """Method that connect to tty port if not connected and send
        according data.

            :returns:  str -- Topic of the message (error or success) and
        Message containing error description or data sent by CC.
        """
        try:
            sleep(USB_RETRY)
            # If we are not connected to TTY port
            if self.serial_connection is None:
                topic, message = self.connect()
            # If we are connected to TTY port
            if self.serial_connection is not None:
                # We wait for a new message on this socket
                data = self.serial_connection.readline()
                # We parse the result
                topic, message = data_validator(
                    data,
                    self.variable_name,
                    self.site_name)
            print self.serial_connection
        except serial.serialutil.SerialException:
            # If during this process, someone deactivate USB connection
            # We reinit serial connection
            topic, message = self.disconnect()
        # At the end we send message
        return topic, message

    def connect(self):
        """Connect serial port to tty.

            :returns:  str -- Topic of the message (error or success) and
        Message containing error description or data sent by CC.
        """
        try:
            # We create a tty connection
            self.serial_connection = serial.Serial(
                self.tty_port,
                BAUDS,
                timeout=self.timeout)
        except OSError:
            # If tty not exist we send according error an retry in a moment
            return ERROR, TTY_CONNECTION_PROBLEM % (
                self.variable_name,
                self.site_name,
                self.tty_port)
        else:
            # When we are connected, we log this success
            info = TTY_CONNECTION_SUCCESS % (
                self.variable_name,
                self.site_name,
                self.tty_port)
            LOGGER.info(info)

    def disconnect(self):
        """Disconnect serial port to tty.

        """
        if self.serial_connection is not None:
            self.serial_connection.close()
            self.serial_connection = None
        # And we log this error
        error = TTY_DISCONNECTED % (
            self.variable_name,
            self.site_name,
            self.tty_port)
        LOGGER.info(error)
        return ERROR, TTY_CONNECTION_PROBLEM % (
            self.variable_name,
            self.site_name,
            self.tty_port)

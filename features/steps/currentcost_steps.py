#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-
# pylint: disable=W0613

"""
    Functionnal test for SMEPI test cases.
"""

#from behave import when, given, then  # pylint: disable-msg=E0611
from behave import when, then  # pylint: disable-msg=E0611
import subprocess
from subprocess import CalledProcessError
from currentcost.utils import error
import pika

BIN = "currentcost"
VAR_NAME = "TEST"
TTY_PORT = "/dev/currentcost"
BAD_TTY_PORT = "/dev/currentcost9876"
MQ_PARAMETER_NAME = "-p"
MQ_PORT = 15001
BAD_MQ_PORT = "ertyu"
LOG_FILE = "logs/currentcost.log"
TTY_ERROR_MESSAGE = "None"
CREDENTIALS = pika.PlainCredentials("admin", "password")
CONNECTION = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', credentials=CREDENTIALS))


def callback(ch, method, properties, body):
    print("Callback => %s" % body)
    assert body == error.TTY_CONNECTION_PROBLEM % (
        VAR_NAME, BAD_TTY_PORT)
    CONNECTION.close()


def check_response_script(commands_response):
    """
        Launch script with parameter.
    """
    for cmdr in commands_response:
        print("Response: %s %s" % (cmdr[0], cmdr[1]))
        assert cmdr[0] is None
        assert cmdr[1] is not None


def launch_script(commands):
    """
        Check response script.
    """
    commands_response = []

    for cmd in commands:
        response = None
        exception = None

        try:
            response = subprocess.check_output(
                cmd, stderr=subprocess.STDOUT, shell=True)
        except CalledProcessError, e:
            exception = e

        commands_response.append((response, exception))

    return commands_response


@when(u'we launch currentcost script without important argument')
def when_launch_script_without_parameter(context):
    """
        Launch currentcost script without important argument.
    """
    commands = [
        ("%s" % BIN),
        ("%s %s" % (BIN, VAR_NAME)),
        ("%s %s" % (BIN, TTY_PORT))
    ]

    context.commands_response = launch_script(commands)


@then(u'we should see an error message on screen')
def error_message_script_without_parameter(context):
    """
        Except that subprocess raise an exception.
    """
    check_response_script(context.commands_response)


@when(u'we launch currentcost script with a bad value for an argument')
def when_launch_script_with_bad_value(context):
    """
        Launch currentcost script with bad value for -p argument.
    """
    commands = [
        ("%s %s %s %s %s" % (
            BIN, VAR_NAME, TTY_PORT, MQ_PARAMETER_NAME, BAD_MQ_PORT))
    ]

    context.commands_response = launch_script(commands)


@then(u'we should see an error message on screen for -p argument')
def error_message_script_with_bad_value(context):
    """
        Except that subprocess raise an exception.
    """
    check_response_script(context.commands_response)


@when(u'we launch currentcost script with unreachable current cost device')
def when_launch_script_with_unreachable(context):
    """
        Launch currentcost script with wrong tty with -p active
    """
    commands = [
        ("%s %s %s %s %s" % (
            BIN, VAR_NAME, BAD_TTY_PORT, MQ_PARAMETER_NAME, MQ_PORT))
    ]

    context.commands_response = launch_script(commands)


@then(u'we should see this error in log')
def detect_unreachability_log(context):
    """
        We should see currentcost unreachability in log file.
    """
    f = open(LOG_FILE, "r")
    lines = f.readlines()
    f.close()
    last_log_file = lines[-1].replace("\n", "").replace("\"", "")
    last_log_file = " ".join(last_log_file.split(" ")[7:])
    assert last_log_file == error.TTY_CONNECTION_PROBLEM % (
        VAR_NAME, BAD_TTY_PORT)


@then(u'we should receive a message saying that current cost is unreachable')
def receive_message_unreachable(context):
    """
        Expect a message saying that currentcost is unreachable on 0MQ.
    """
    channel = CONNECTION.channel()
    channel.queue_declare(queue='error')
    try:
        channel.basic_consume(callback, queue='error', no_ack=True)
        channel.start_consuming()
    except pika.exceptions.ConnectionClosed:
        pass

#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-
# pylint: disable=W0613

"""
    Functionnal test for SMEPI test cases.
"""

#from behave import when, given, then  # pylint: disable-msg=E0611
from __future__ import print_function
from behave import when, then  # pylint: disable-msg=E0611
import subprocess
from subprocess import CalledProcessError
from currentcost.utils import error_utils
import pika
import shlex
from time import sleep


BIN = "currentcost"
VAR_NAME = "TEST_electric_meter"
SITE_NAME = "TEST_liogen_home"
ARGUMENT_TTY_PORT = "--tty-port"
TTY_PORT = "/dev/currentcost"
BAD_TTY_PORT = "/dev/currentcost9876"
ARGUMENT_MQ_CREDENTIAL = "--rabbitMQ-credential"
MQ_CREDENTIAL = "admin:password"
BAD_MQ_CREDENTIAL = "admzfzein:paszeasword"
MQ_HOST = "localhost"
LOG_FILE = "logs/currentcost.log"
TTY_ERROR_MESSAGE = "None"
CREDENTIALS = pika.PlainCredentials("admin", "password")
CONNECTION = pika.BlockingConnection(
    pika.ConnectionParameters(host=MQ_HOST, credentials=CREDENTIALS))


def callback(channel, method, properties, body):
    """
        Callback called when a new message is available.
    """
    print("Callback => %s" % body)
    assert body == error_utils.TTY_CONNECTION_PROBLEM % (
        VAR_NAME, SITE_NAME, BAD_TTY_PORT)
    CONNECTION.close()


def check_response_script(commands_response):
    """
        Launch script with parameter.
    """
    for cmdr in commands_response:
        print("Response: %s" % cmdr)
        assert cmdr is not None


def thread_subprocess():
    """
        Launch a subprocess in a non blocking way.
    """
    pass


def launch_script(commands):
    """
        Launch script in a subprocess.
    """
    commands_response = []

    for cmd in commands:
        exception = None

        try:
            subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
        except CalledProcessError, error:
            exception = error

        commands_response.append(exception)

    return commands_response


@when(u'we launch currentcost script without important argument')
def when_launch_without_parameter(context):
    """
        Launch currentcost script without important argument.
    """
    commands = [
        ("%s" % BIN),
        ("%s %s" % (BIN, VAR_NAME)),
        ("%s %s" % (BIN, SITE_NAME)),
        ("%s %s" % (BIN, TTY_PORT))
    ]

    context.commands_response = launch_script(commands)


@then(u'we should see an error message on screen')
def error_script_without_parameter(context):
    """
        Except that subprocess raise an exception.
    """
    check_response_script(context.commands_response)


@when(u'we start currentcost with bad port without rabbitmq')
def when_launch_with_unreachable(context):
    """
        Launch currentcost script with wrong tty with -p active
    """
    commands = "%s %s %s %s %s" % (
        BIN, VAR_NAME, SITE_NAME, ARGUMENT_TTY_PORT, BAD_TTY_PORT)
    process = subprocess.Popen(
        shlex.split(commands),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    sleep(5)
    process.terminate()


@when(u'we start currentcost with bad port and bad rabbitmq credential')
def launch_ccunreach_badrmq(context):
    """
        Launch unreachable currentcost with bad rabbitmq credential
    """
    commands = "%s %s %s %s %s %s %s" % (
        BIN, VAR_NAME, SITE_NAME, ARGUMENT_TTY_PORT, BAD_TTY_PORT,
        ARGUMENT_MQ_CREDENTIAL, BAD_MQ_CREDENTIAL)
    process = subprocess.Popen(
        shlex.split(commands),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    sleep(5)
    process.terminate()


@then(u'we should see currentcost is unreachable in log')
def detect_unreachability_log(context):
    """
        We should see currentcost unreachability in log file.
    """
    log_file = open(LOG_FILE, "r")
    lines = log_file.readlines()
    log_file.close()
    last_log_file = lines[-1].replace("\n", "").replace("\"", "")
    last_log_file = " ".join(last_log_file.split(" ")[9:])
    error = error_utils.TTY_CONNECTION_PROBLEM % (
        VAR_NAME, SITE_NAME, BAD_TTY_PORT)
    print("Last line => %s" % last_log_file)
    print("Expect => %s" % error)
    assert last_log_file == error


@then(u'we should see rabbitmq error in log')
def detect_rabbitmqerror_log(context):
    """
        We should see currentcost unreachability in log file.
    """
    log_file = open(LOG_FILE, "r")
    lines = log_file.readlines()
    log_file.close()
    last_log_file = lines[-2].replace("\n", "").replace("\"", "")
    last_log_file = " ".join(last_log_file.split(" ")[9:])
    error = error_utils.RABBIT_MQ_CREDENTIAL_PROBLEM % (
        BAD_MQ_CREDENTIAL.split(":")[0],
        BAD_MQ_CREDENTIAL.split(":")[1],
        MQ_HOST)
    print("Last line => %s" % last_log_file)
    print("Expect => %s" % error)
    assert last_log_file == error


@when(u'we start currentcost with bad port with rabbitmq')
def launch_ccunreach_withoutrmq(context):
    """
        Launch currentcost script with wrong tty with -p active
    """
    commands = "%s %s %s %s %s %s %s" % (
        BIN, VAR_NAME, SITE_NAME, ARGUMENT_TTY_PORT, BAD_TTY_PORT,
        ARGUMENT_MQ_CREDENTIAL, MQ_CREDENTIAL)
    process = subprocess.Popen(shlex.split(commands))
    sleep(1)
    process.terminate()


@then(u'we should receive a message saying that current cost is unreachable')
def receive_message_unreachable(context):
    """
        Expect a message saying that currentcost is unreachable on 0MQ.
    """
    channel = CONNECTION.channel()
    channel.queue_declare(queue=error_utils.ERROR)
    try:
        channel.basic_consume(callback, queue=error_utils.ERROR, no_ack=True)
        channel.start_consuming()
    except pika.exceptions.ConnectionClosed:
        pass

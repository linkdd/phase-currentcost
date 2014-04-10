#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-
# pylint: disable=W0613

"""
    Functionnal test for SMEPI test cases.
"""

from __future__ import print_function
from behave import when, then, given  # pylint: disable-msg=E0611
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
TTY_PORT = "tests/tty/currentcost"
BAD_TTY_PORT = "/dev/currentcost9876"
ARGUMENT_MQ_CREDENTIAL = "--rabbitMQ-credential"
MQ_CREDENTIAL = "admin:password"
BAD_MQ_CREDENTIAL = "admzfzein:paszeasword"
MQ_HOST = "localhost"
LOG_FILE = "logs/currentcost.log"
TTY_ERROR_MESSAGE = "None"
CREDENTIALS = pika.PlainCredentials("admin", "password")
SOCAT = "socat"
SIMULATED_TTY_PORT = "PTY,link=%s" % TTY_PORT
SIMULATED_TTY_PORT2 = "PTY,link=tests/tty/writer"
CONNECTION = pika.BlockingConnection(
    pika.ConnectionParameters(host=MQ_HOST, credentials=CREDENTIALS))
CURRENTCOST_MESSAGE = "<msg><src>CC128-v1.29</src><dsb>00786</dsb><time>00:31:36</time><tmpr>19.3</tmpr><sensor>0</sensor><id>00077</id><type>1</type><ch1><watts>00405</watts></ch1></msg>"



def check_cc_unreachable(channel, method, properties, body):
    """
        Callback called when a new message is available.
    """
    print("check_cc_unreachable => %s" % body)
    assert body == error_utils.TTY_CONNECTION_PROBLEM % (
        VAR_NAME, SITE_NAME, BAD_TTY_PORT)
    CONNECTION.close()


def check_cc_unreachable2(channel, method, properties, body):
    """
        Callback called when a new message is available.
    """
    print("check_cc_unreachable => %s" % body)
    assert body == error_utils.TTY_CONNECTION_PROBLEM % (
        VAR_NAME, SITE_NAME, TTY_PORT)
    CONNECTION.close()


def check_cc_disconected(channel, method, properties, body):
    """
        Callback called when a new message is available.
    """
    print("check_cc_disconected => %s" % body)
    assert body == error_utils.CURRENTCOST_TIMEOUT % (
        VAR_NAME, SITE_NAME)
    CONNECTION.close()


def check_response_script(commands_response):
    """
        Launch script with parameter.
    """
    for cmdr in commands_response:
        print("Response: %s" % cmdr)
        assert cmdr is not None


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


@when(u"we launch currentcost script without important argument")
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


@then(u"we should see an error message on screen")
def error_script_without_parameter(context):
    """
        Except that subprocess raise an exception.
    """
    check_response_script(context.commands_response)


@when(u"we start currentcost with bad port without rabbitmq")
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


@when(u"we start currentcost with bad port and bad rabbitmq credential")
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


@then(u"we should see currentcost is unreachable in log")
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


@then(u"we should see rabbitmq error in log")
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


@when(u"we start currentcost with bad port with rabbitmq")
def launch_ccunreach_withoutrmq(context):
    """
        Launch currentcost script with wrong tty port.
    """
    commands = "%s %s %s %s %s %s %s" % (
        BIN, VAR_NAME, SITE_NAME, ARGUMENT_TTY_PORT, BAD_TTY_PORT,
        ARGUMENT_MQ_CREDENTIAL, MQ_CREDENTIAL)
    process = subprocess.Popen(shlex.split(commands))
    sleep(1)
    process.terminate()


@then(u"we should receive a message saying that current cost is unreachable")
def receive_message_unreachable(context):
    """
        Expect a message saying that currentcost is unreachable on RabbitMQ.
    """
    channel = CONNECTION.channel()
    channel.queue_declare(queue=error_utils.ERROR)
    try:
        channel.basic_consume(
            check_cc_unreachable,
            queue=error_utils.ERROR,
            no_ack=True)
        channel.start_consuming()
    except pika.exceptions.ConnectionClosed:
        pass


@given(u"current cost does not send any message")
def simulate_cc_disconnected(context):
    """
        Simulate USB port connection with socat.
    """
    commands = "%s %s %s" % (SOCAT, SIMULATED_TTY_PORT, SIMULATED_TTY_PORT2)
    context.socat = subprocess.Popen(shlex.split(commands))


@when(u"we launch currentcost script and reach the timeout limit")
def cc_reach_timeout(context):
    """
        Launch currentcost script.
    """
    commands = "%s %s %s %s %s %s %s" % (
        BIN, VAR_NAME, SITE_NAME, ARGUMENT_TTY_PORT, TTY_PORT,
        ARGUMENT_MQ_CREDENTIAL, MQ_CREDENTIAL)
    context.process = subprocess.Popen(shlex.split(commands))


@then(u"we should get informed that current cost does not send messages")
def rmq_no_messages(context):
    """
        Waited on RabbitMQ an error message saying that current cost
        does not send any message.
    """
    CONNECTION = pika.BlockingConnection(
        pika.ConnectionParameters(host=MQ_HOST, credentials=CREDENTIALS))
    channel = CONNECTION.channel()
    channel.queue_declare(queue=error_utils.ERROR)
    try:
        channel.basic_consume(
            check_cc_disconected,
            queue=error_utils.ERROR,
            no_ack=True)
        channel.start_consuming()
    except pika.exceptions.ConnectionClosed:
        pass

    context.process.terminate()
    context.socat.terminate()


@then(u"we should see current cost does not send any message in log")
def log_no_messages(context):
    """
        Waited to see in log that current cost does not send any messages.
    """
    log_file = open(LOG_FILE, "r")
    lines = log_file.readlines()
    log_file.close()
    last_log_file = lines[-1].replace("\n", "").replace("\"", "")
    last_log_file = " ".join(last_log_file.split(" ")[9:])
    error = error_utils.CURRENTCOST_TIMEOUT % (
        VAR_NAME, SITE_NAME)
    print("Last line => %s" % last_log_file)
    print("Expect => %s" % error)
    assert last_log_file == error


@given(u"current cost is connected and currentcost script is launched")
def cc_launch_correctly(context):
    """
        Current cost tty port is created with socat and we launch currentcost
        script.
    """
    commands = "%s %s %s" % (SOCAT, SIMULATED_TTY_PORT, SIMULATED_TTY_PORT2)
    context.socat = subprocess.Popen(shlex.split(commands))

    commands = "%s %s %s %s %s %s %s" % (
        BIN, VAR_NAME, SITE_NAME, ARGUMENT_TTY_PORT, TTY_PORT,
        ARGUMENT_MQ_CREDENTIAL, MQ_CREDENTIAL)
    context.process = subprocess.Popen(shlex.split(commands))

    sleep(3)

    log_file = open(LOG_FILE, "r")
    lines = log_file.readlines()
    log_file.close()
    last_log_file = lines[-1].replace("\n", "").replace("\"", "")
    last_log_file = " ".join(last_log_file.split(" ")[9:])
    error = error_utils.TTY_CONNECTION_SUCCESS % (
        VAR_NAME, SITE_NAME, TTY_PORT)
    print("Last line => %s" % last_log_file)
    print("Expect => %s" % error)
    assert last_log_file == error


@when(u"we disconnect USB port")
def usb_port_disconnection(context):
    """
        Simulation of an USB port disconnection killing socat process.
    """
    context.socat.terminate()


@then(u"we should receive a message saying that current cost is disconnected")
def receive_message_disconnected(context):
    """
        Expect a message saying that currentcost is unreachable on RabbitMQ.
    """
    CONNECTION = pika.BlockingConnection(
        pika.ConnectionParameters(host=MQ_HOST, credentials=CREDENTIALS))
    channel = CONNECTION.channel()
    channel.queue_declare(queue=error_utils.ERROR)
    try:
        channel.basic_consume(
            check_cc_unreachable2,
            queue=error_utils.ERROR,
            no_ack=True)
        channel.start_consuming()
    except pika.exceptions.ConnectionClosed:
        pass
    context.process.terminate()


@then(u"we should see currentcost is disconnected in log")
def detect_disconnected_log(context):
    """
        We should see currentcost unreachability in log file.
    """
    log_file = open(LOG_FILE, "r")
    lines = log_file.readlines()
    log_file.close()
    last_log_file = lines[-1].replace("\n", "").replace("\"", "")
    last_log_file = " ".join(last_log_file.split(" ")[9:])
    error = error_utils.TTY_CONNECTION_PROBLEM % (
        VAR_NAME, SITE_NAME, TTY_PORT)
    print("Last line => %s" % last_log_file)
    print("Expect => %s" % error)
    assert last_log_file == error

#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-
# pylint: disable=W0613

"""
    Functionnal test for this project.
"""

from __future__ import print_function
from behave import when, then, given  # pylint: disable=E0611
import subprocess
from subprocess import CalledProcessError
from currentcost.utils import CC_INCORRECT_MESSAGE, TTY_CONNECTION_PROBLEM
from currentcost.utils import CURRENTCOST_TIMEOUT, RABBIT_MQ_CREDENTIAL_PROBLEM
from currentcost.utils import ERROR, SUCCESS, TTY_CONNECTION_SUCCESS
import pika
import shlex
from time import sleep, tzname
import serial
import json
import logging
import logging.config
from tests.fixtures.history import HISTORY_1, HISTORY_2, HISTORY_3, HISTORY_4
from tests.fixtures.history import HISTORY_5, HISTORY_6, HISTORY_7, HISTORY_8
from tests.fixtures.history import HISTORY_9, HISTORY_10, HISTORY_11
from tests.fixtures.history import HISTORY_12, HISTORY_13


DEFAULT_LOG_FILE = "logs/log.conf"
logging.config.fileConfig(DEFAULT_LOG_FILE)
LOGGER = logging.getLogger("currentcost")

BIN = "phase-currentcost"
VAR_NAME = "TEST_electric_meter"
SITE_NAME = "TEST_liogen_home"
ARGUMENT_TTY_PORT = "--tty-port"
TTY_PORT = "tests/tty/currentcost"
BAD_TTY_PORT = "/dev/currentcost9876"
TTY_WRITER_PORT = "tests/tty/writer"
ARGUMENT_MQ_CREDENTIAL = "--rabbitmq-credential"
MQ_CREDENTIAL = "admin:password"
BAD_MQ_CREDENTIAL = "admzfzein:paszeasword"
MQ_HOST = "localhost"
ARGUMENT_LOG_CONF = "--log-conf"
LOG_CONF = "logs/log.conf"
LOG_FILE = "logs/phase-currentcost.log"
SUDO_LOG_FILE = "/var/log/phase/phase-currentcost.log"
TTY_ERROR_MESSAGE = "None"
CREDENTIALS = pika.PlainCredentials("admin", "password")
SOCAT = "socat"
SIMULATED_TTY_PORT = "PTY,link=%s" % TTY_PORT
SIMULATED_TTY_PORT2 = "PTY,link=%s" % TTY_WRITER_PORT
CONNECTION = pika.BlockingConnection(
    pika.ConnectionParameters(host=MQ_HOST, credentials=CREDENTIALS))
CURRENTCOST_MESSAGE = "<msg><src>CC128-v1.29</src><dsb>00786</dsb>\
<time>00:31:36</time><tmpr>19.3</tmpr><sensor>0</sensor><id>00077</id>\
<type>1</type><ch1><watts>00405</watts></ch1></msg>"
WRONG_CURRENTCOST_MESSAGE = "<msg><src>ensor>0</sensor><id>00077</id>\
<type>1</type><ch1><watts>00405</watts></ch1></msg>"
HISTORYS = (
    HISTORY_1,
    HISTORY_2,
    HISTORY_3,
    HISTORY_4,
    HISTORY_5,
    HISTORY_6,
    HISTORY_7,
    HISTORY_8,
    HISTORY_9,
    HISTORY_10,
    HISTORY_11,
    HISTORY_12,
    HISTORY_13)
RECEIVE_HISTORY = []


def verify_json_message(body, expected_message):
    """
        Verify JSON message value.
    """
    message = json.loads(body)
    assert message["message"] == expected_message
    assert message["siteID"] == SITE_NAME
    assert message["variableID"] == VAR_NAME
    assert message["dstTimezone"] == tzname[1]
    assert message["nonDstTimezone"] == tzname[0]


def extract_from_log(expected_message, log_file_path, line):
    """
        Method that extract expecting line from log and compare
        to expected_message
    """
    log_file = open(log_file_path, "r")
    lines = log_file.readlines()
    log_file.close()
    body = lines[line]
    print("1. => %s" % body)
    body = " ".join(body.split(" ")[9:])[:-2]
    print("2. => %s" % body)

    try:
        verify_json_message(body, expected_message)
    except ValueError:
        message = body
        assert message == expected_message


def consume(topic, callback):
    """
        Method that wait for a message on RabbitMQ topics channels.
    """
    channel = CONNECTION.channel()
    channel.queue_declare(queue=topic)
    try:
        channel.basic_consume(
            callback,
            queue=topic,
            no_ack=True)
        channel.start_consuming()
    except pika.exceptions.ConnectionClosed:
        pass


def check_history_message(channel, method, properties, body):
    """
        Callback that check historical message sent.
    """
    RECEIVE_HISTORY.append(body)
    array_size = "check_history_message => len %d" % len(RECEIVE_HISTORY)
    LOGGER.info(array_size)
    index = len(RECEIVE_HISTORY) - 1

    expected_message = HISTORYS[index]
    verify_json_message(body, expected_message)
    channel.close()


def check_cc_message(channel, method, properties, body):
    """
        Callback called when a new message is available.
    """
    expected_message = CURRENTCOST_MESSAGE
    verify_json_message(body, expected_message)
    channel.close()


def check_cc_incorrect(channel, method, properties, body):
    """
        Callback that check incorrect message sent.
    """
    expected_message = CC_INCORRECT_MESSAGE % (
        VAR_NAME,
        SITE_NAME,
        WRONG_CURRENTCOST_MESSAGE)
    verify_json_message(body, expected_message)
    channel.close()


def check_cc_unreachable(channel, method, properties, body):
    """
        Callback called when a new message is available.
    """
    expected_message = TTY_CONNECTION_PROBLEM % (
        VAR_NAME,
        SITE_NAME,
        BAD_TTY_PORT)
    verify_json_message(body, expected_message)
    channel.close()


def check_cc_disconnected(channel, method, properties, body):
    """
        Callback called when a new message is available.
    """
    expected_message = TTY_CONNECTION_PROBLEM % (
        VAR_NAME,
        SITE_NAME,
        TTY_PORT)
    verify_json_message(body, expected_message)
    channel.close()


def check_usb_disconnected(channel, method, properties, body):
    """
        Callback called when a new message is available.
    """
    expected_message = CURRENTCOST_TIMEOUT % (VAR_NAME, SITE_NAME)
    verify_json_message(body, expected_message)
    channel.close()


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


@when("we launch currentcost script without important argument")
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


@then("we should see an error message on screen")
def error_script_without_parameter(context):
    """
        Except that subprocess raise an exception.
    """
    check_response_script(context.commands_response)


@when("we start currentcost with bad port without rabbitmq")
def when_launch_with_unreachable(context):
    """
        Launch currentcost script with wrong tty port
    """
    commands = "%s %s %s %s %s %s %s" % (
        BIN,
        VAR_NAME,
        SITE_NAME,
        ARGUMENT_TTY_PORT,
        BAD_TTY_PORT,
        ARGUMENT_LOG_CONF,
        LOG_CONF)
    process = subprocess.Popen(shlex.split(commands))
    sleep(5)
    process.terminate()


@when("we start currentcost with bad port and bad rabbitmq credential")
def launch_ccunreach_badrmq(context):
    """
        Launch unreachable currentcost with bad rabbitmq credential
    """
    commands = "%s %s %s %s %s %s %s %s %s" % (
        BIN,
        VAR_NAME,
        SITE_NAME,
        ARGUMENT_TTY_PORT,
        BAD_TTY_PORT,
        ARGUMENT_MQ_CREDENTIAL,
        BAD_MQ_CREDENTIAL,
        ARGUMENT_LOG_CONF,
        LOG_CONF)
    process = subprocess.Popen(shlex.split(commands))
    sleep(5)
    process.terminate()


@then("we should see currentcost is unreachable in log")
def detect_unreachability_log(context):
    """
        We should see currentcost unreachability in log file.
    """
    error = TTY_CONNECTION_PROBLEM % (
        VAR_NAME, SITE_NAME, BAD_TTY_PORT)
    extract_from_log(error, LOG_FILE, -1)


@then("we should see rabbitmq error in log")
def detect_rabbitmqerror_log(context):
    """
        We should see currentcost unreachability in log file.
    """
    error = RABBIT_MQ_CREDENTIAL_PROBLEM % (
        BAD_MQ_CREDENTIAL.split(":")[0],
        BAD_MQ_CREDENTIAL.split(":")[1],
        MQ_HOST)
    extract_from_log(error, LOG_FILE, -2)


@when("we start currentcost with bad port with rabbitmq")
def launch_ccunreach_withoutrmq(context):
    """
        Launch currentcost script with wrong tty port.
    """
    commands = "%s %s %s %s %s %s %s %s %s" % (
        BIN,
        VAR_NAME,
        SITE_NAME,
        ARGUMENT_TTY_PORT,
        BAD_TTY_PORT,
        ARGUMENT_MQ_CREDENTIAL,
        MQ_CREDENTIAL,
        ARGUMENT_LOG_CONF,
        LOG_CONF)
    context.process = subprocess.Popen(shlex.split(commands))
    sleep(1)


@then("we should receive a message saying that current cost is unreachable")
def receive_message_unreachable(context):
    """
        Expect a message saying that currentcost is unreachable on RabbitMQ.
    """
    context.process.terminate()
    consume(ERROR, check_cc_unreachable)


@given("current cost does not send any message")
def simulate_cc_disconnected(context):
    """
        Simulate USB port connection with socat.
    """
    commands = "%s %s %s" % (SOCAT, SIMULATED_TTY_PORT, SIMULATED_TTY_PORT2)
    context.socat = subprocess.Popen(shlex.split(commands))


@when("we launch currentcost script and reach the timeout limit")
def cc_reach_timeout(context):
    """
        Launch currentcost script.
    """
    commands = "%s %s %s %s %s %s %s %s %s" % (
        BIN,
        VAR_NAME,
        SITE_NAME,
        ARGUMENT_TTY_PORT,
        TTY_PORT,
        ARGUMENT_MQ_CREDENTIAL,
        MQ_CREDENTIAL,
        ARGUMENT_LOG_CONF,
        LOG_CONF)
    context.process = subprocess.Popen(shlex.split(commands))


@then("we should get informed that current cost does not send messages")
def rmq_no_messages(context):
    """
        Waited on RabbitMQ an error message saying that current cost
        does not send any message.
    """
    consume(ERROR, check_usb_disconnected)
    context.process.terminate()
    context.socat.terminate()


@then("we should see current cost does not send any message in log")
def log_no_messages(context):
    """
        Waited to see in log that current cost does not send any messages.
    """
    error = CURRENTCOST_TIMEOUT % (
        VAR_NAME, SITE_NAME)
    extract_from_log(error, LOG_FILE, -1)


@given("current cost is connected and currentcost script is launched")
def cc_launch_correctly(context):
    """
        Current cost tty port is created with socat and we launch currentcost
        script.
    """
    commands = "%s %s %s" % (SOCAT, SIMULATED_TTY_PORT, SIMULATED_TTY_PORT2)
    context.socat = subprocess.Popen(shlex.split(commands))

    commands = "%s %s %s %s %s %s %s %s %s" % (
        BIN,
        VAR_NAME,
        SITE_NAME,
        ARGUMENT_TTY_PORT,
        TTY_PORT,
        ARGUMENT_MQ_CREDENTIAL,
        MQ_CREDENTIAL,
        ARGUMENT_LOG_CONF,
        LOG_CONF)
    context.process = subprocess.Popen(shlex.split(commands))

    sleep(3)

    error = TTY_CONNECTION_SUCCESS % (
        VAR_NAME, SITE_NAME, TTY_PORT)
    extract_from_log(error, LOG_FILE, -1)


@when("we disconnect USB port")
def usb_port_disconnection(context):
    """
        Simulation of an USB port disconnection killing socat process.
    """
    context.socat.terminate()


@then("we should receive a message saying that current cost is disconnected")
def receive_message_disconnected(context):
    """
        Expect a message saying that currentcost is unreachable on RabbitMQ.
    """
    consume(ERROR, check_cc_disconnected)
    context.process.terminate()


@then("we should see currentcost is disconnected in log")
def detect_disconnected_log(context):
    """
        We should see currentcost unreachability in log file.
    """
    error = TTY_CONNECTION_PROBLEM % (
        VAR_NAME, SITE_NAME, TTY_PORT)
    extract_from_log(error, LOG_FILE, -1)


@given("current cost is connected and script is launched")
def cc_connected_launched(context):
    """
        We simulate a socket with socat and launch cc script.
    """
    commands = "%s %s %s" % (SOCAT, SIMULATED_TTY_PORT, SIMULATED_TTY_PORT2)
    context.socat = subprocess.Popen(shlex.split(commands))

    sleep(1)

    commands = "%s %s %s %s %s %s %s %s %s" % (
        BIN,
        VAR_NAME,
        SITE_NAME,
        ARGUMENT_TTY_PORT,
        TTY_PORT,
        ARGUMENT_MQ_CREDENTIAL,
        MQ_CREDENTIAL,
        ARGUMENT_LOG_CONF,
        LOG_CONF)
    context.process = subprocess.Popen(shlex.split(commands))


@when("current cost send instant consumption")
def send_instant_consumption(context):
    """
        Launch cc script with RabbitMQ activated.
    """
    sleep(1)
    context.ser = serial.Serial(TTY_WRITER_PORT)
    context.ser.write("%s\n" % CURRENTCOST_MESSAGE)


@then("we should receive instant consumption over the network")
def send_receive_message(context):
    """
        Send a message on socket and retrieve it on RabbitMQ.
    """
    consume(SUCCESS, check_cc_message)
    context.ser.close()
    context.process.terminate()
    context.socat.terminate()


@when("current cost send incorrect message")
def send_incorrect_message(context):
    """
        Send incorrect message over socket.
    """
    sleep(1)

    ser = serial.Serial(TTY_WRITER_PORT)
    ser.write("%s\n" % WRONG_CURRENTCOST_MESSAGE)

    sleep(1)

    ser.close()
    context.process.terminate()
    context.socat.terminate()


@then("we should get informed that current cost send incorrect message")
def receive_incorrect_message(context):
    """
        Receive incorrect message error through RabbitMQ.
    """
    consume(ERROR, check_cc_incorrect)


@then("we should see incorrect message error in log")
def log_incorrect_message(context):
    """
        Verify in log that we see error.
    """
    error = CC_INCORRECT_MESSAGE % (
        VAR_NAME, SITE_NAME, WRONG_CURRENTCOST_MESSAGE)
    extract_from_log(error, LOG_FILE, -1)


@then("we should receive historical consumption over the network")
def receive_historical_consumption(context):
    """
        Receive historical consumption.
    """

    sleep(1)
    ser = serial.Serial(TTY_WRITER_PORT)

    for hist in HISTORYS:
        ser.write("%s" % hist)

        consume(SUCCESS, check_history_message)

    ser.close()
    context.process.terminate()
    context.socat.terminate()


@when("we start currentcost with bad port without rabbitmq with log")
def sudo_log_badport_message(context):
    """Start a process in sudo mode with global log.conf.

    """
    commands = "%s %s %s %s %s %s" % (
        "sudo",
        BIN,
        VAR_NAME,
        SITE_NAME,
        ARGUMENT_TTY_PORT,
        BAD_TTY_PORT)
    process = subprocess.Popen(shlex.split(commands))
    sleep(5)
    process.terminate()


@then("we should see currentcost is unreachable in /var/log")
def sudo_log_cc_unreachable(context):
    """Verify in /var/log that currentcost is unreachable.

    """
    error = TTY_CONNECTION_PROBLEM % (
        VAR_NAME, SITE_NAME, BAD_TTY_PORT)
    extract_from_log(error, SUDO_LOG_FILE, -1)

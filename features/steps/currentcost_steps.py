#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-
# pylint: disable=W0613

"""
    Functionnal test for SMEPI test cases.
"""

from behave import when, given, then  # pylint: disable-msg=E0611
import subprocess
from subprocess import CalledProcessError
from currentcost.utils import error

BIN = "currentcost"
VAR_NAME = "TEST"
TTY_PORT = "/dev/currentcost"

@when(u'we launch currentcost script without important argument')
def script_without_parameter(context):
    """
        Launch currentcost script without important argument.
    """
    context.cmds = [
        ([BIN], "script_response_any"),
        ([BIN, VAR_NAME], "script_response_tty"),
        ([BIN, TTY_PORT], "script_response_var_name"),
        ([BIN, VAR_NAME, TTY_PORT], "script_response_var_name")
    ]
    
    context.cmds_response = []
    
    for cmd in context.cmds:
        response = None
        exception = None
        
        try:
            response = subprocess.check_output(cmd[0], stderr=subprocess.STDOUT, shell=True)
        except CalledProcessError, e:
            exception = e

        context.cmds_response.append((response, exception))


@then(u'we should see an error message on screen')
def error_message_script_without_parameter(context):
    """
        Except that subprocess raise an exception.
    """
    for cmdr in context.cmds_response:
        print("Response: %s %s" % (cmdr[0], cmdr[1]))
        assert cmdr[0] is None
        assert cmdr[1] is not None

@when(u'we launch currentcost script with a bad value for an argument')
def script_with_bad_value(context):
    """
        Launch currentcost script with bad value for -p argument.
    """
    assert False

@then(u'we should see an error message on screen for -p argument')
def error_message_script_with_bad_value(context):
    """
        Except that subprocess raise an exception.
    """
    assert False

@given(u'current cost is unreachable')
def given_currentcost_unreachable(context):
    """
        Select a bad TTY port to simulate currentcost unreachability.
    """
    assert False

@when(u'we launch currentcost script')
def when_launch_currentcost_script(context):
    """
        Launch currentcost script with wrong tty with -p active
    """
    assert False

@then(u'we should receive a message saying that current cost is unreachable')
def receive_message_unreachable(context):
    """
        Expect a message saying that currentcost is unreachable on 0MQ.
    """
    assert False


@then(u'we should see this error in log')
def detect_unreachability_log(context):
    """
        We should see currentcost unreachability in log file.
    """
    assert False

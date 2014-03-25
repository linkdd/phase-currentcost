"""
    Functionnal test for SMEPI test cases.
"""

#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-
# pylint: disable=W0613

from behave import when, given, then  # pylint: disable-msg=E0611
import subprocess

@when(u'we launch currentcost script without important argument')
def script_without_parameter(context):
    """
        Launch currentcost script without important argument.
    """
    context.script_response_any = subprocess.check_output(["currentcost"])
    context.script_response_tty = subprocess.check_output(["currentcost", "--variable-name", "TEST"])
    context.script_response_var_name = subprocess.check_output(["currentcost", "--tty-name", "/dev/currentcost"])


@then(u'we should see an error message on screen and in log')
def error_message_script_without_parameter(context):
    """
        Script error message.
    """
    print("Response: %s" % context.script_response_any)
    print("Response: %s" % context.script_response_tty)
    print("Response: %s" % context.script_response_var_name)
    assert context.script_response_any == 'ErrorMissingVariableName: missing variable name parameter!'
    assert context.script_response_tty == 'ErrorMissingTTYParameter: missing tty parameter!'
    assert context.script_response_var_name == 'ErrorMissingVariableName: missing variable name parameter!'

#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""
    Global error shared across this project.
"""

ERROR = "error"

ERROR_TOO_FEW_ARGUMENTS = "usage: currentcost [-h] [-p PORT] [-v]" \
    " variable_name tty\ncurrentcost: error: too few arguments"

ERROR_BAD_VALUE_ARGUMENTS = "usage: currentcost [-h] [-p PORT] [-v]" \
    " variable_name tty\ncurrentcost: error: argument -p/--port: " \
    "invalid int value: '%s'"

TTY_CONNECTION_PROBLEM = "CurrentCost %s: TTY connection problem: %s " \
    "is unreachable"

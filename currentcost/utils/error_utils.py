#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""
    Global error shared across this project.
"""

TOPIC = "currentcost"

ERROR = "error"

TTY_CONNECTION_PROBLEM = "CurrentCost %s in %s: TTY connection problem: %s " \
    "is unreachable. Retry connection in 5 seconds."

TTY_TRYING_CONNECTION = "CurrentCost %s in %s: Trying to connect to %s."

TTY_CONNECTION_SUCCESS = "CurrentCost %s in %s: Success connection to %s."

TTY_DISCONNECTED = "CurrentCost %s in %s: TTY port %s disconnected."

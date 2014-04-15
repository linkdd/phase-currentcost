#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""
    Global error shared across this project.
"""

SUCCESS = "currentcost"

ERROR = "error"

TTY_CONNECTION_PROBLEM = "CurrentCost %s in %s: TTY connection problem: %s \
is unreachable. Retry connection in 5 seconds."

TTY_TRYING_CONNECTION = "CurrentCost %s in %s: Trying to connect to %s."

TTY_CONNECTION_SUCCESS = "CurrentCost %s in %s: Success connection to %s."

TTY_DISCONNECTED = "CurrentCost %s in %s: TTY port %s disconnected."

CURRENTCOST_TIMEOUT = "CurrentCost %s in %s: Reach timeout. Verify \
CurrentCost wire connection or wave range"

CC_INCORRECT_MESSAGE = "CurrentCost %s in %s: Send incorrect\
 message => %s."

RABBIT_MQ_CONNECTION_PROBLEM = "Problem trying to connect to RabbitMQ with \
this configuration: username: %s, password: %s, host: %s"

RABBIT_MQ_CREDENTIAL_PROBLEM = "Problem bad RabbitMQ credential with \
this configuration: username: %s, password: %s, host: %s"

CURRENTCOST_UNICODE_ERROR = "Bad message sent from currentcost, invalid ASCII"

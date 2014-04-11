#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""
    Global error shared across this project.
"""

SUCCESS = u"currentcost"

ERROR = u"error"

TTY_CONNECTION_PROBLEM = u"CurrentCost %s in %s: TTY connection problem: %s \
is unreachable. Retry connection in 5 seconds."

TTY_TRYING_CONNECTION = u"CurrentCost %s in %s: Trying to connect to %s."

TTY_CONNECTION_SUCCESS = u"CurrentCost %s in %s: Success connection to %s."

TTY_DISCONNECTED = u"CurrentCost %s in %s: TTY port %s disconnected."

CURRENTCOST_TIMEOUT = u"CurrentCost %s in %s: Reach timeout. Verify \
CurrentCost wire connection or wave range"

RABBIT_MQ_CONNECTION_PROBLEM = u"Problem trying to connect to RabbitMQ with \
this configuration: username: %s, password: %s, host: %s"

RABBIT_MQ_CREDENTIAL_PROBLEM = u"Problem bad RabbitMQ credential with \
this configuration: username: %s, password: %s, host: %s"

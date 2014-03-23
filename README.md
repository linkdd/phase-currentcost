=============
pyCurrentCost
=============

Functionnal test with fixtures to simulate CurrentCost on port COM and waited for currentCost to send messages.

Usage
=====

    $ plugwise_util -h
    Usage: plugwise_util [options]

    Options:
        -h, --help                      Show this help message and exit.
        -m PORT, --mq-port=PORT         Socket port to publish to MQ.
        -v NAME, --variable-name=NAME   Name of the variable.
        -t TTY, --tty-name=TTY          TTY port to connect to current cost.
        -v, --verbose                   Activate verbose mode.

Example: currentcost --variable-name=test --mq-port=5001 --tty-name=currentcost 

Development process
===================

In this project, we will try to use the best pratices of the development.

Scenario based design
---------------------

* Take a paper and write what you code should do and how it sould do using a story.

Document driven-design
----------------------

* Take a minute and update documentation
* Then define a clear release roadmap 
* Update README.md, CHANGELOG.txt, TODO.md

Behavior driven development
---------------------------

* Add functional test

Test driven development
-----------------------

* Add unit test while you don't pass functional test
* Develop function has you don't pass unit test

Code versioning
---------------

* Commit after each new implemented function
* Create a release after each validation of functional test

Workflow
========

Nominal case
------------

* N1: Start service
    * E1: Service doesn't start. Send an error message over the network and log this error.
* N2: Arguments analysis
    * E2: Missing argument. Return an error and log it
    * E3: Bad value for an argument. Return and error and log it
* N3: Connexion to current cost
    * E4: Unable to connect to current cost. Send a message over the network to inform that it is not possible to connect to current cost and log it. Return to step N3.
* N4: Waited for a message from current cost
    * E5: If no message received after 30 seconds, send a message over the network to inform that there is a problem with current cost and log it. Return to step N4.
* N5: XML message received and analysed
    * E6: Incorrect message. Log this message and return to step N4. (to be defined)
* N6: Creation of a network message looking like {variableID: ..., date: ..., message: ...}
* N7: Send this message over the network.
    * E7: Problem during message sending. Retry and log this error.
* N8: Message sent over the network. Return to step N4.

Alternative cases
-----------------

* A1: USB port disconected. Log this error, send an error message over the network and retry to reconnect to the USB port. If USB port reconnected, return to step N2.
* A2: Receive a message that ask for shutdown the service. Log this demand and properly close this program. (to be defined)

Test plan
=========

Look at features/currentcost.feature

=============
pyCurrentCost
=============

Functional test with fixtures to simulate CurrentCost on port COM and waited for currentCost to send messages.

Usage
=====

    $ currentcost -h
    Usage: currentcost [options]

    Options:
        -h, --help                      Show this help message and exit.
        -m PORT, --mq-port=PORT         Socket port to publish to MQ.
        -v NAME, --variable-name=NAME   Name of the variable.
        -t TTY, --tty-name=TTY          TTY port to connect to current cost.
        -v, --verbose                   Activate verbose mode.

Example: 

    currentcost --variable-name=test --mq-port=5001 --tty-name=/dev/currentcost -v

Development process
===================

In this project, we will try to use the best practices of the development.

* **Scenario based design** 
    * Take a paper and write what you code should do and how it should do using a story.
* **Document driven-design**
    * Take a minute and update documentation
    * Then define a clear release road map 
    * Update README.md, CHANGELOG.txt, TODO.md
* **Behavior driven development**
    * Add one functional test
* **Test driven development**
    * Add unit test while you don't pass functional test
    * Develop function has you don't pass unit test
* **Code version**
    * Commit after each new implemented function
    * Create a release after each validation of functional test
* **Refactoring**
    * Refactor code to improve readability, avoid code redundancy, speed compute time
    * Return to BDD part.

Work flow
=========

Nominal case
------------

* N1: Service started
* N2: Arguments analysis
    * E1: Missing argument. Return an error and log it
    * E2: Bad value for an argument. Return and error and log it
* N3: Connexion to current cost
    * E3: Unable to connect to current cost. Send a message over the network to inform that it is not possible to connect to current cost and log it. Return to step N3.
* N4: Waited for a message from current cost
    * E4: If no message received after 30 seconds, send a message over the network to inform that there is a problem with current cost and log it. Return to step N4.
* N5: XML message received and analyzed
    * E5: Incorrect message. Log this message and return to step N4. (to be defined)
* N6: Creation of a network message looking like {variableID: ..., date: ..., message: ...}
* N7: Send this message over the network.
    * E6: Problem during message sending. Retry and log this error.
* N8: Message sent over the network. Return to step N4.

Alternative cases
-----------------

* A1: USB port disconnected. Log this error, send an error message over the network and retry to reconnect to the USB port. If USB port reconnected, return to step N2.

Test plan
=========

Look at features/currentcost.feature

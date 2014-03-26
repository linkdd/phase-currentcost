=============
pyCurrentCost
=============

Functional test with fixtures to simulate CurrentCost on port COM and waited for currentCost to send messages.

TO BE COMPLETED (goals of the project)

Dependencies
============

TO BE COMPLETED

Installation
============

TO BE COMPLETED

Usage
=====

    $ currentcost -h
    usage: currentcost [-h] [-p PORT] [-v] variable_name tty

    positional arguments:
      variable_name         name of the variable
      tty                   tty port to connect to current cost

    optional arguments:
      -h, --help            show this help message and exit
      -p PORT, --port PORT  socket port to publish to 0MQ
      -v, --verbose         activate verbose mode

Examples: 

To see the current consumption on Current cost (or redirect stdout to a file to keep a log) use:

    currentcost test /dev/currentcost -v

To redirect Current Cost message to 0MQ and connect one or several others processes to use this message use:   

    currentcost test /dev/currentcost --port=5001

To redirect Current Cost message to 0MQ and see display in console:   

    currentcost test /dev/currentcost --port=5001 -v


Development process
===================

Philosophy
----------

In this project, we will try to use the best practices of the development.

* **Scenario based design** 
    * Take a paper and write what you code should do and how it should do using a story. (DESCRIBE MORE)
* **Document driven-design**
    * Take a minute and update documentation before coding (global documentation, code comment, test comment).
    * Always keep a clear release road map. Update it if needed. 
    * Update README.md, CHANGELOG.txt, TODO.md as soon as possible.
* **Behavior driven development**
    * Add one functional test.
* **Test driven development**
    * Add one unit test while you don't pass this functional test
    * Develop function while you don't pass this unit test
* **Code version**
    * Commit after each new implemented function
    * Create a release after each validation of functional test
* **Refactoring**
    * Refactor code to improve readability, avoid code redundancy, speed compute time
    * Return to BDD part.

Setup environment
-----------------

* **IDEA: Explain virtualenv and virtualenvwrapper**
* **IDEA: Create a init script that ask several question and bootstrap project (plug-in)**
* **IDEA: generate_setup to use sdist command**
* **IDEA: test new plugin creation on TimeSeriesLogger**
* **IDEA: move pyCurrentCost.py outside of phase**
* **IDEA: phase in development should provide init script to init and register new plugin**


**TO BE COMPLETED**

Work flow
=========

**TO BE MOVED**

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

**TO BE MOVED**

**IDEA: Link to features/currentcost.feature**

Look at features/currentcost.feature

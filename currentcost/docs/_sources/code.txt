Modules
=======

Workflow
--------

Here is a description of the main script workflow with error and succes out.

**Nominal case**

N1: Service started and arguments analysis
    * **E1**: Missing argument. Return an error and log it
    * **E2**: Bad value for an argument. Return and error and log it
N2: Connexion to current cost
    * **E3**: Unable to connect to current cost. Send a message over the network to inform that it is not possible to connect to current cost and log it. Return to step N3.
N3: Waited for a message from current cost
    * **E4**: If no message received after 30 seconds, send a message over the network to inform that there is a problem with current cost and log it. Return to step N4.
N4: XML message received and analyzed
    * **E5**: Incorrect message. Log this message and return to step N4. (to be defined)
N5: Creation of a network message looking like {variableID: ..., date: ..., message: ...} and send this message over the network. Return to step N4.
    * **E6**: Problem during message sending. Retry and log this error.

**Alternative cases**

A1: USB port disconnected.
    * **E7**: Log this error, send an error message over the network and retry to reconnect to the USB port. If USB port reconnected, return to step N2.

Test plan
---------

Here is a description of test made using behave to validate this software.

.. literalinclude:: ../../features/currentcost.feature


Utils module
------------

This project contains 2 mains modules:
    * Utils contains all useful functions and Variables for this project,
    * RabbitMQ_messager send message to RabbitMQ or display it in stdout.

.. automodule:: currentcost.utils
    :members:

RabbitMQ_messager module
------------------------

.. automodule:: currentcost.messager
 
.. autoclass:: RabbitMQMessager
    :members:
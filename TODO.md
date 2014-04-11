Release v1.0.0
==============

Objectives
----------
    
Launch a current cost program on command line, read data from a current cost and send message over the network.

Tasks
-----

* CurrentCost connection:
    * Add timezone to data send

* Project:
    * Architecture:
        * Fix clone
        * Create log util file to add init and activate verbose mode on it
        * Move log.conf and currentcost.log in /opt/phase/
        * Refactor architecture of this project (Think what should be a class, what should be a method, ...)
        * Change error_utils to a more accurate name
    * Deployment:
        * Modify installation to perform custom installation following this advice http://stackoverflow.com/questions/15853058/run-custom-task-when-call-pip-install
        * After installation modification, change log configuration place.
        * Work on deployment (look at pip install, pip freeze, pip bundle, pip wheel)
    * Documentation:
        * Comment all the code
        * Add list of message send using RabbitMQ in README (success message, error message, ...)
        * Detail process to start in development mode
        * Generate proper documenation
        * Complete dosctrings using https://github.com/claws/txCurrentCost/blob/master/txcurrentcost/monitor.py example
    * Tests:
        * Split currentcost_steps.py into several test file
        * Integrate code on travis
        * Develop current cost simulator (simple version, should be a specific project in the future)
    * Development:
        * Fix paver watch problem (stop watch, don't take into account bin/currentcost) (try to use with fabric)
        * Launch a server web in a subprocess.Popen
        * Launch watch task in a subprocess.Popen
        * Listen for a terminating command to quit properly two previous subprocesses

* Message file:
    * Add func test for: rabbitMQ is not started, rabbitMQ is disconnected during currentcost is running
    * This exception is raised when we stop RabbitMQ during currentcost script is running =>AttributeError: 'BlockingConnection' object has no attribute 'disconnect'
    * This exception is raised when we try to connect to RabbitMQ and RabbitMQ is disconnected => pika.exceptions.AMQPConnectionError: 1
    * Test application with RabbitMQ disconnected (find a way to automatize this)

* Blog:
    * Current Cost and explain this choice comparing to other product
    * pyCurrentCost and how to use it
    * RabbitMQ and comparison to 0MQ
    * pySerial and socat
    * BDD
    * TDD
    * Scenario based design
    * ...


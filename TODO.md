Release v1.0.0
==============

Objectives
----------
    
Launch a current cost program on command line, read data from a current cost and send message over the network.

Tasks
-----

* CurrentCost connection:
    * Add timezone to data send method (verify UTC hour)

* Message file:
    * Add func test for: rabbitMQ is not started, rabbitMQ is disconnected during currentcost is running
    * This exception is raised when we stop RabbitMQ during currentcost script is running =>AttributeError: 'BlockingConnection' object has no attribute 'disconnect'
    * This exception is raised when we try to connect to RabbitMQ and RabbitMQ is disconnected => pika.exceptions.AMQPConnectionError: 1
    * Test application with RabbitMQ disconnected (find a way to automatize this)
    * Integrate code on travis
    * Fix paver watch problem (stop watch, don't take into account bin/currentcost) (try to use with fabric)
    * Launch a server web in a subprocess.Popen
    * Launch watch task in a subprocess.Popen
    * Listen for a terminating command to quit properly two previous subprocesses

* News:
    * add parameter to target log.conf path for test (by default it should be /opt/phase/currentcost/log.conf)
    * add parameter to create currentcost.log for test (by default it should be /var/log/phase/currentcost.log)
    * Modify installation to perform custom installation following this advice http://stackoverflow.com/questions/15853058/run-custom-task-when-call-pip-install
    * During currentcost installation: 
        * Create /opt/phase/currentcost/log.conf and /var/log/phase/currentcost.log files.
        * Install RabbitMQ
        * Install pip dependencies
    * Work on deployment (look at pip install, pip freeze, pip bundle, pip wheel), install log.conf in /opt/phase/currentcost/ and currentcost.log in /var/log/phase

* Documentation:
    * Comment all the code
    * Add list of message send using RabbitMQ in README (success message, error message, ...)
    * Detail process to start in development mode
    * Generate proper documenation
    * Complete dosctrings using https://github.com/claws/txCurrentCost/blob/master/txcurrentcost/monitor.py example
    * Describe development process
    * Describe usage process
    * List all features

* Refactoring:
    * Fix clone
    * Create log util file to add init and activate verbose mode on it
    * Refactor architecture of this project (Think what should be a class, what should be a method, ...)
    * Change error_utils to a more accurate name
    * Split currentcost_steps.py into several test file
    * Extract messager from this project and create a pip to install it for several phase module

* Blog:
    * Current Cost and explain this choice comparing to other product
    * pyCurrentCost and how to use it
    * RabbitMQ and comparison to 0MQ
    * pySerial and socat
    * BDD
    * TDD
    * Scenario based design
    * ...


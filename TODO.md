====
TODO
====

Release v1.0.0
==============

Objectives
----------
    
Launch a current cost program on command line, read data from a current cost and send message over the network.

Tasks application
-----------------

* Message file:
    
    * Add unit test for this class
    * Add func test in case or wrong username/password in RabbitMQ
    * Add func test for: rabbitMQ is not started, rabbitMQ is disconnected during currentcost is running
    * This exception is raised when we stop RabbitMQ during currentcost script is running =>AttributeError: 'BlockingConnection' object has no attribute 'disconnect'
    * This exception is raised when we try to connect to RabbitMQ and RabbitMQ is disconnected => pika.exceptions.AMQPConnectionError: 1

* Project:
    * Detail process to start in development mode
    * Modify installation to perform custom installation following this advice http://stackoverflow.com/questions/15853058/run-custom-task-when-call-pip-install
    * Move log.conf and currentcost.log in /opt/phase/
    * After installation modification, change log configuration place.
    * Test application with RabbitMQ disconnected (find a way to automatize this)
    * Refactor architecture of this project (Think what should be a class, what should be a method, ...)
    * Work on deployment (look at pip install, pip freeze, pip bundle, pip wheel)
    * Change error_utils to a more accurate name
    * Test retry currentcost connection if USB port is not reachable (wait 5 seconds)
    * Integrate code on travis
    * Fix paver watch problem (stop watch, don't take into account bin/currentcost) (try to use with fabric)
    * Launch a server web in a subprocess.Popen
    * Launch watch task in a subprocess.Popen
    * Listen for a terminating command to quit properly two previous subprocesses
    * Develop current cost simulator (simple version, should be a specific project in the future)

* CurrentCost connection:
    * Add timeout to currentcost readlines
    * Validate XML message from currentcost
    * Write objectives and test case for message waited
    * Develop method that waited for message to current cost + error case + unit test
    * Write objectives and test case for message convertion and send over the network (look at express for tis part)
    * Develop method that convert XML message to network message + error case  + unit test
    * Develop and test script that integrate all this part
    * Generate proper documenation
    * Complete dosctrings using https://github.com/claws/txCurrentCost/blob/master/txcurrentcost/monitor.py example



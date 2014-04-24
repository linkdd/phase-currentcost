TODO v1.0.0
===========

Objectives
----------
    
Launch a current cost program on command line, read data from a current cost and send message over the network.

Schedule
--------

* For April, 18th 2014:
    * Create currentcost class
    * Add production test in behave and launch it only on travis

Pending tasks
-------------

* Message file:
    * Add func test for: rabbitMQ is not started, rabbitMQ is disconnected during currentcost is running
    * This exception is raised when we stop RabbitMQ during currentcost script is running =>AttributeError: 'BlockingConnection' object has no attribute 'disconnect'
    * This exception is raised when we try to connect to RabbitMQ and RabbitMQ is disconnected => pika.exceptions.AMQPConnectionError: 1
    * Test application with RabbitMQ disconnected (find a way to automatize this)

* News:
    
    * Work on deployment (look at pip install, pip freeze, pip bundle, pip wheel)
    * Fix paver watch problem (stop watch) (try to use with fabric)
    * Launch a server web in a subprocess.Popen
    * Launch watch task in a subprocess.Popen
    * Listen for a terminating command to quit properly two previous subprocesses
    * Support of python 3.2, 3.3, pypy

* Documentation:
    * Detail process to start in development mode
    * Describe development process (look at paver main page http://paver.github.io/paver/)
    * Describe usage process
    * List all features
    * Write README.rst
    * Split README.rst in several file

* Refactoring:
    * Split currentcost_steps.py into several test file
    * Comment test files
    * Extract messager from this project and create a pip to install it for several phase module


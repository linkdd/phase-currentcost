TODO v1.0.0
===========

Objectives
----------
    
Launch a current cost program on command line, read data from a current cost and send message over the network.

Schedule
--------

* For April, 25th 2014:
    * List all features
    * Write README.rst
    * Describe usage process
    * Add link to ReadTheDoc

Pending tasks
-------------

* phase-messager:
    * Extract messager from this project and create a pip to install it for several phase module
    * Add func test for: rabbitMQ is not started, rabbitMQ is disconnected during currentcost is running
    * This exception is raised when we stop RabbitMQ during currentcost script is running =>AttributeError: 'BlockingConnection' object has no attribute 'disconnect'
    * This exception is raised when we try to connect to RabbitMQ and RabbitMQ is disconnected => pika.exceptions.AMQPConnectionError: 1
    * Test application with RabbitMQ disconnected (find a way to automatize this)

* phase
    * Documentation:
        * Detail process to start in development mode
        * Describe development process (look at paver main page http://paver.github.io/paver/)
    * Functionalities:
        * Fix paver watch problem (stop watch) (try to use with fabric)
        * Launch a server web in a subprocess.Popen
        * Launch watch task in a subprocess.Popen
        * Listen for a terminating command to quit properly two previous subprocesses

* News:
    * Support of python 3.2, 3.3, pypy
    * Integrate improved pavement.py
    * Integrate phase-messager instead of messager

* Refactoring:
    * Split currentcost_steps.py into several test file
    * Comment test files
    


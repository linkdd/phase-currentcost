====
TODO
====

Release v1.0.0
==============

Objectives
----------
    
Launch a current cost program on command line that read data from a current cost and send message over the network.

Tasks
-----

* Fix paver watch problem (stop watch, don't take into account bin/currentcost) (try to use with fabric)
* Retry currentcost connection if USB port is disconnected (wait 5 seconds)
* Find a way to launch subprocess in an non blocking way (in a thread, and kill it after test)
* Write objectives and test case for message waited
* Develop method that waited for message to current cost + error case + unit test
* Write objectives and test case for message convertion and send over the network (look at express for tis part)
* Develop method that convert XML message to network message + error case  + unit test
* Develop and test script that integrate all this part
* Generate proper documenation
* Complete dosctrings using https://github.com/claws/txCurrentCost/blob/master/txcurrentcost/monitor.py example
* Migrate changelog.txt to Changelog.md with markdown support

Need
----

* Develop current cost simulator (simple version, should be a specific project in the future)


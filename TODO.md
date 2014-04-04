====
TODO
====

Release v1.0.0
==============

Objectives
----------
    
Launch a current cost program on command line that read data from a current cost and send message over the network.

Tasks application
-----------------

* Add timeout to currentcost readlines
* Change error_utils to a more accurate name
* Retry currentcost connection if USB port is not reachable (wait 5 seconds)
* Validate XML message from currentcost
* Write objectives and test case for message waited
* Develop method that waited for message to current cost + error case + unit test
* Write objectives and test case for message convertion and send over the network (look at express for tis part)
* Develop method that convert XML message to network message + error case  + unit test
* Develop and test script that integrate all this part
* Generate proper documenation
* Complete dosctrings using https://github.com/claws/txCurrentCost/blob/master/txcurrentcost/monitor.py example
* Migrate changelog.txt to Changelog.md with markdown support

Tasks building development environment
--------------------------------------

* Fix paver watch problem (stop watch, don't take into account bin/currentcost) (try to use with fabric)
* Launch a server web in a subprocess.Popen
* Launch watch task in a subprocess.Popen
* Listen for a terminating command to quit properly two previous subprocesses
* Develop current cost simulator (simple version, should be a specific project in the future)


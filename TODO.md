====
TODO
====

Release v1.0.0
==============

Objectives
----------
    
Launch a current cost program on command line that read data from a current cost simulator

Tasks
-----

* Fix sdist method in paver
* Study Paver and setuptools to create a develop installed version in virtualenv to test script as $> currentcost and use it in behave file.
* Create error global variable script to share Error
* Write objectives and test case for argument parser
* Develop method that parse argument + verify error case + unit test
* Write objectives and test case for current cost connection
* Develop method that connect to current cost + error case + unit test
* Write objectives and test case for message waited
* Develop method that waited for message to current cost + error case + unit test
* Write objectives and test case for message convertion and send over the network (look at express for tis part)
* Develop method that convert XML message to network message + error case  + unit test
* Write objectives and test case for messaging module
* Develop and test script that integrate all this part 

Need
----

* Develop current cost simulator (simple version, should be a specific project in the future)


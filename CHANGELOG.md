phase-currentcost (v0.9.4) stable; urgency=low
--------------------------------------------

* Integration on travis
* Create log util file to add init and activate verbose mode on it
* Refactor architecture of this project (Think what should be a class, what should be a method, ...)
* Change error_utils to a more accurate name
* Documentation: Comment all the code

Pierre Leray <pierreleray64@gmail.com>  2014-04-16 14:30:00

phase-currentcost (v0.9.3) stable; urgency=low
--------------------------------------------

* Fix pylint error and warning
* Fix clone
* Send timezone with data
* Refactor currentcost script

Pierre Leray <pierreleray64@gmail.com>  2014-04-14 17:00:00

phase-currentcost (v0.9.2) stable; urgency=low
--------------------------------------------

* Improve TODO.md and define new target.
* Fix rename problem.

Pierre Leray <pierreleray64@gmail.com>  2014-04-13 20:00:00

phase-currentcost (v0.9.1) stable; urgency=low
--------------------------------------------

* Test manually currentcost script strength.
* Fix unicode encoding error.

Pierre Leray <pierreleray64@gmail.com>  2014-04-11 19:00:00

phase-currentcost (v0.9.0) stable; urgency=low
--------------------------------------------

* Funct test current cost historical consumption message.

Pierre Leray <pierreleray64@gmail.com>  2014-04-11 17:30:00

phase-currentcost (v0.8.0) unstable; urgency=low
--------------------------------------------

* Funct test current cost incorrect message.

Pierre Leray <pierreleray64@gmail.com>  2014-04-11 16:30:00

phase-currentcost (v0.7.0) unstable; urgency=low
--------------------------------------------

* Funct test current cost instant consumption message.

Pierre Leray <pierreleray64@gmail.com>  2014-04-11 12:30:00

phase-currentcost (v0.6.0) unstable; urgency=low
--------------------------------------------

* Funct test current cost usb disconnected.

Pierre Leray <pierreleray64@gmail.com>  2014-04-10 23:50:00

phase-currentcost (v0.5.0) unstable; urgency=low
--------------------------------------------

* Funct test current cost disconnected and reach timeout.

Pierre Leray <pierreleray64@gmail.com>  2014-04-10 22:20:00

phase-currentcost (v0.4.1) unstable; urgency=low
--------------------------------------------

* Add date to currentcost message.

Pierre Leray <pierreleray64@gmail.com>  2014-04-07 16:25:00

phase-currentcost (v0.4.0) unstable; urgency=low
--------------------------------------------

* Make a difference between credential error and host error
* Add func test in case of non activation of RabbitMQ
* Add func test in case or wrong username/password in RabbitMQ

Pierre Leray <pierreleray64@gmail.com>  2014-04-07 16:10:00

phase-currentcost (v0.3.9) unstable; urgency=low
--------------------------------------------

* Fix print problem in stdout

Pierre Leray <pierreleray64@gmail.com>  2014-04-07 11:45:00

phase-currentcost (v0.3.8) unstable; urgency=low
--------------------------------------------

* Update todo

Pierre Leray <pierreleray64@gmail.com>  2014-04-07 11:25:00

phase-currentcost (v0.3.7) unstable; urgency=low
--------------------------------------------

* Add unit test to rabbitmq_messager.py
* Fix error in with non terminating process in currentcost_steps.py
* Add new RabbitMQ error

Pierre Leray <pierreleray64@gmail.com>  2014-04-07 11:20:00

phase-currentcost (v0.3.6) unstable; urgency=low
--------------------------------------------

* Create a class for RabbitMQ messages
* If support of RabbitMQ is not activated, we print message on stdout
* Put username and password of RabbitMQ into parameter

Pierre Leray <pierreleray64@gmail.com>  2014-04-06 22:00:00

phase-currentcost (v0.3.5) unstable; urgency=low
--------------------------------------------

* Change currentcost script api
* Put log file into parameter
* Put username and password of RabbitMQ into parameter
* Parameter strategies is:
    * default log is /opt/phase/currentcost.log
    * default rabbitMQ username is 'admin'
    * default rabbitMQ password id 'password'
    * default tty port is /dev/currentcost
    * all of this parameter are optional and could be over-writted, (except for log)

Pierre Leray <pierreleray64@gmail.com>  2014-04-06 21:20:00

phase-currentcost (v0.3.4) unstable; urgency=low
--------------------------------------------

* Add serial tty read
* Update setup.py
* Retrieve and print CurrentCost message

Pierre Leray <pierreleray64@gmail.com>  2014-04-04 16:00:00

phase-currentcost (v0.3.3) unstable; urgency=low
--------------------------------------------

* Add site_name script parameter

Pierre Leray <pierreleray64@gmail.com>  2014-04-04 15:15:00

phase-currentcost (v0.3.2) unstable; urgency=low
--------------------------------------------

* Launch subprocess with Popen to avoid blocking testing

Pierre Leray <pierreleray64@gmail.com>  2014-04-04 14:50:00

phase-currentcost (v0.3.1) unstable; urgency=low
--------------------------------------------

* Remove 0MQ port command and code affiliated

Pierre Leray <pierreleray64@gmail.com>  2014-04-04 14:30:00

phase-currentcost (v0.3.0) unstable; urgency=low
--------------------------------------------

* Write objectives and test case for current cost connection
* Develop method that connect to current cost + error case + unit test
* Integration with RabbitMQ
* Write objectives and test case for messaging module

Pierre Leray <pierreleray64@gmail.com>  2014-04-02 00:00:00

phase-currentcost (v0.2.3) unstable; urgency=low
--------------------------------------------

* Add method to send error message over the network
* Test log error

Pierre Leray <pierreleray64@gmail.com>  2014-03-28 16:30:00

phase-currentcost (v0.2.2) unstable; urgency=low
--------------------------------------------

* Add logging message during init of program
* Add functional test to return error when wrong -p parameter value

Pierre Leray <pierreleray64@gmail.com>  2014-03-28 11:00:00

phase-currentcost (v0.2.1) unstable; urgency=low
--------------------------------------------

* Add function to test bad parameter for -p option
* Add function to test current cost unreachability

Pierre Leray <pierreleray64@gmail.com>  2014-03-27 23:20:00

phase-currentcost (v0.2.0) unstable; urgency=low
--------------------------------------------

* Write objectives and test case for argument parser
* Develop method that parse argument + verify error case + unit test
* Pass parser functional test

Pierre Leray <pierreleray64@gmail.com>  2014-03-26 15:30:00

phase-currentcost (v0.1.10) unstable; urgency=low
---------------------------------------------

* Add logger
* Add first version of argument parsing
* Improve README.md

Pierre Leray <pierreleray64@gmail.com>  2014-03-26 11:00:00

phase-currentcost (v0.1.9) unstable; urgency=low
--------------------------------------------

* Create error global variable script to share Error

Pierre Leray <pierreleray64@gmail.com>  2014-03-26 11:00:00

phase-currentcost (v0.1.8) unstable; urgency=low
--------------------------------------------

* Test global install on virtualenv

Pierre Leray <pierreleray64@gmail.com>  2014-03-25 11:45:00

phase-currentcost (v0.1.7) unstable; urgency=low
--------------------------------------------

* Fix sdist method in paver
* Study Paver and setuptools to create a develop installed version in virtualenv to test script as $> currentcost and use it in behave file.

Pierre Leray <pierreleray64@gmail.com>  2014-03-25 11:00:00

phase-currentcost (v0.1.6) unstable; urgency=low
--------------------------------------------

* Write code to test features

Pierre Leray <pierreleray64@gmail.com>  2014-03-24 23:30:00

phase-currentcost (v0.1.5) unstable; urgency=low
--------------------------------------------

* Write usage on README.md
* Write test plan on README.md
* Write features 

Pierre Leray <pierreleray64@gmail.com>  2014-03-24 00:00:00

phase-currentcost (v0.1.4) unstable; urgency=low
--------------------------------------------

* Improve TODO.md 

Pierre Leray <pierreleray64@gmail.com>  2014-03-23 17:30:00

phase-currentcost (v0.1.3) unstable; urgency=low
--------------------------------------------

* Project creation
* Paver configuration
* Improve documentation
* Prepare development 

Pierre Leray <pierreleray64@gmail.com>  2014-03-23 15:30:00
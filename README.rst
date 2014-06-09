=================
phase-currentcost
=================

.. image:: http://img.shields.io/travis/liogen/phase-currentcost.png?branch=master
    :target: https://travis-ci.org/liogen/phase-currentcost
    :alt: Travis CI Build Status

.. image:: http://img.shields.io/pypi/v/phase-currentcost.png
    :target: https://pypi.python.org/pypi/phase-currentcost
    :alt: Latest Version

.. image:: http://img.shields.io/pypi/dm/phase-currentcost.png
    :target: https://pypi.python.org/pypi/phase-currentcost
    :alt: Downloads

.. image:: http://img.shields.io/badge/license-MIT-red.png
    :target: https://github.com/liogen/phase-currentcost
    :alt: License

CurrentCost data collector script for phase project.

`CurrentCost EnviR 128 <http://www.currentcost.com/product-envir.html>`_ is an appliance that monitor your electricity consumption and provide an `API <http://www.currentcost.com/cc128/xml.htm>`_ to retrieve data from USB cable.

phase-currentcost allow use to retrieve data from usb cable using `pyserial <http://pyserial.sourceforge.net/>`_ and transmit information to stdout or to `RabbitMQ <https://www.rabbitmq.com/>`_ using `Pika <http://pika.readthedocs.org/en/latest/>`_ module. 

More precisly, this script collect instantaneous and historical data from Current Cost. It also take care of usb disconnection, Current Cost bad message format, timeout and power disconnection and send an error on stdout or on RabbitMQ each time for later anlysis. Also it create an udev rule to transform /dev/ttyUSB* to /dev/currentcost for serial port connection.

For more information, full documentation is available on `readthedocs.org <http://phase-currentcost.readthedocs.org/en/latest/>`_

Installation
------------

Requirements:

  * Platform: Unix (only tested on Ubuntu 12.04)
  * Python 2.7
  * Pip (last version)
  * RabbitMQ (last version)

To install this software, you need to install python 2.7 and pip

.. code-block:: bash
  
  $ sudo apt-get install python python-pip
  $ sudo pip install --upgrade pip

Then, you have to install and configure RabbitMQ (change "admin" and "password" by your credential)

.. code-block:: bash
  
  $ USERNAME="admin"
  $ PASSWORD="password" 
  $ echo "deb http://www.rabbitmq.com/debian/ testing main" > sudo /etc/apt/sources.list.d/rabbitmq.list
  $ wget http://www.rabbitmq.com/rabbitmq-signing-key-public.asc
  $ sudo apt-key add rabbitmq-signing-key-public.asc
  $ sudo apt-get update
  $ sudo apt-get install rabbitmq-server -y
  $ sudo service rabbitmq-server start
  # If you get a 'command not found' error for this line, use /usr/lib/rabbitmq/bin/rabbitmq-plugins instead
  $ sudo rabbitmq-plugins enable rabbitmq_management
  $ sudo rabbitmqctl add_user $USERNAME $PASSWORD
  $ sudo rabbitmqctl set_user_tags $USERNAME administrator
  $ sudo rabbitmqctl set_permissions -p / $USERNAME ".*" ".*" ".*"
  $ sudo rabbitmqctl delete_user guest
  $ sudo service rabbitmq-server restart

Then you can install phase-currentcost

.. code-block:: bash
  
  $ sudo pip install phase-currentcost

Usage
-----

.. code-block:: bash

    $ sudo phase-currentcost -h
    usage: phase-currentcost [-h] [-c /path/to/config.ini]

    optional arguments:
      -l LOG_CONF, --log-conf LOG_CONF
                            path to log configuration
      -v, --verbose         activate verbose mode

Configuration
-------------

.. code-block:: ini

    # Configure current cost plugin
    [currentcost]

    ## Variable's name
    # variable_name = 

    ## Name of the variable's location
    # site_name =

    ## TTY port to connect to current cost
    # tty_port = 


    # Configure how data are sent to RabbitMQ
    [rabbitmq]

    enabled = true
    url = amqp://guest:guest@127.0.0.1:5672/

    # Configure Canopsis compatibility mode
    [canopsis]

    enabled = false

    connector = phase
    connector_name = currentcost
    component = $siteID
    resource = $variableID


By default:

* We targetting /dev/currentcost as tty port.
* RabbitMQ is not activated. We send message to stdout so you can collect it on file. If you want to share your message over the network using RabbitMQ, you can activate this function by enabling it in the configuration file.
* Log configuration file is located in /opt/phase/phase-currentcost.conf and log file is in /var/logs/phase/phase-currentcost.log. You can set log configuration file using -l option with a path to your log.conf file.

Examples
--------

To see the current consumption on Current cost on stdout use this config file:

.. code-block:: ini

    [currentcost]

    variable_name = electric_meter
    site_name = liogen_home
    tty_port = /dev/currentcost


.. code-block:: bash
    
    $ sudo phase-currentcost -c currentcost.ini
    {"variableID": "electric_meter", "dstTimezone": "UTC", "siteID": "liogen_home", "date": "2014-04-25T12:00:17.754959", "message": "CurrentCost electric_meter in liogen_home: TTY connection problem: /dev/currentcost is unreachable. Retry connection in 5 seconds.", "nonDstTimezone": "UTC"} 
    {"variableID": "electric_meter", "dstTimezone": "UTC", "siteID": "liogen_home", "date": "2014-04-25T12:00:22.769256", "message": "CurrentCost electric_meter in liogen_home: TTY connection problem: /dev/currentcost is unreachable. Retry connection in 5 seconds.", "nonDstTimezone": "UTC"}
    {"variableID": "electric_meter", "dstTimezone": "UTC", "siteID": "liogen_home", "date": "2014-04-25T12:00:22.769256", "message": "<msg><src>CC128-v1.29</src><dsb>00786</dsb><time>00:31:36</time><tmpr>19.3</tmpr><sensor>0</sensor><id>00077</id><type>1</type><ch1><watts>00405</watts></ch1></msg>", "nonDstTimezone": "UTC"}

With rabbitMQ message over the network with verbose mode activated:

.. code-block:: ini

    [currentcost]

    variable_name = electric_meter
    site_name = liogen_home
    tty_port = /dev/currentcost

    [rabbitmq]

    enabled = true
    url = amqp://admin:password@127.0.0.1:5672/

.. code-block:: bash

    $ sudo phase-currentcost -c currentcost.ini -v
    Starting current cost application
    Current time: 2014-04-25 12:01:34.350781
    Variable name: electric_meter
    Site name: liogen_home
    TTY port: /dev/currentcost

    {"variableID": "electric_meter", "dstTimezone": "UTC", "siteID": "liogen_home", "date": "2014-04-25T12:00:22.769256", "message": "<msg><src>CC128-v1.29</src><dsb>00786</dsb><time>00:31:36</time><tmpr>19.3</tmpr><sensor>0</sensor><id>00077</id><type>1</type><ch1><watts>00405</watts></ch1></msg>", "nonDstTimezone": "UTC"}
    {"variableID": "electric_meter", "dstTimezone": "UTC", "siteID": "liogen_home", "date": "2014-04-25T12:00:22.769256", "message": "<msg><src>CC128-v1.29</src><dsb>00786</dsb><time>00:31:36</time><tmpr>19.3</tmpr><sensor>0</sensor><id>00077</id><type>1</type><ch1><watts>00405</watts></ch1></msg>", "nonDstTimezone": "UTC"}

Message send through RabbitMQ
-----------------------------

A message is a JSON containing this properties:

:variableID: Name of the variable
:siteID: Name of the site
:date: Date in UTC
:dstTimezone: Timezone with DST
:nonDstTimezone: Timezone without DST
:message: Message to deliver through RabbitMQ

Messages list:

+-------------+---------------------------------+---------------------------------------------------+ 
| Channel     | Message                         | Description                                       |
+=============+=================================+===================================================+ 
| error       | utils.TTY_CONNECTION_PROBLEM    | Send when TTY port is not reachable               |
+-------------+---------------------------------+---------------------------------------------------+
| error       | utils.CURRENTCOST_TIMEOUT       | Send when TTY port is connected but reach timeout |
+-------------+---------------------------------+---------------------------------------------------+
| error       | utils.CC_INCORRECT_MESSAGE      | Send when Currentcost send an invalid message     |
+-------------+---------------------------------+---------------------------------------------------+
| currentcost | CurrentCost XML message         | Send Currentcost XML message                      |
+-------------+---------------------------------+---------------------------------------------------+

When Canopsis mode is enabled, message sent through RabbitMQ respect the event specification of Canopsis.

Contribute
----------

I am more than happy to accept external contributions like feedback, bug reports and pull requests. 

Do not hesitate to post an `issue <https://github.com/liogen/phase-currentcost/issues>`_ if you have any problem to install or to use this software.

You can also use this way to ask for a Feature request. I am also available to answer you on `Stack Overflow <http://stackoverflow.com/questions/tagged/phase-currentcost>`_

Here is the development process to test and validate your features.

1. Prepare your development environment:

    .. code-block:: bash

        # `Socat <http://www.dest-unreach.org/socat/>`_ is usefull to create socket connection between 2 files.
        $ sudo apt-get install socat vim git-core
        # Install virtualenv and virtualenvwrapper if it's not done.
        $ sudo pip install virtualenvwrapper
        $ mkdir ~/.virtualenvs
        $ vim ~/.bashrc
        # Modify your ~/.bashrc and add this 2 lines:
        # export WORKON_HOME=~/.virtualenvs
        # source /usr/local/bin/virtualenvwrapper.sh
        $ bash

2. Go on `github <https://github.com/liogen/phase-currentcost>`_ and fork this project.

3. Clone it on your conputer:

    .. code-block:: bash

        $ cd <your_workspace>
        $ git clone git@github.com:<username>/phase-currentcost.git
        $ git checkout develop

4. Prepare your virtualenv

    .. code-block:: bash

        $ mkvirtualenv phase
        (phase)$ pip install paver
        (phase)$ paver prepare

5. Add functional or unit tests

6. Code your features

7. To validate your implementation, launch:

    .. code-block:: bash

        (phase)$ paver validate

8. Modify Todo, Changelog and update documentation

9. Commit and push on github:

    .. code-block:: bash

        (phase)$ git add .
        (phase)$ git commit -a -m "<your commit message>"
        (phase)$ git push origin develop  

10. Propose a pull request on github

License
-------

The MIT License (MIT)

Copyright (c) 2014 Pierre Leray

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

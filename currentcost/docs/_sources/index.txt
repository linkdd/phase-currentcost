.. pyCurrentCost documentation master file, created by
   sphinx-quickstart on Sat Mar 22 12:59:45 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

=================
phase-currentcost
=================

CurrentCost data collector script for phase project.

`CurrentCost EnviR 128 <http://www.currentcost.com/product-envir.html>`_ is an appliance that monitor your electricity consumption and provide an `API <http://www.currentcost.com/cc128/xml.htm>`_ to retrieve data from USB cable.

phase-currentcost allow use to retrieve data from usb cable using `pyserial <http://pyserial.sourceforge.net/>`_ and transmit information to stdout or to `RabbitMQ <https://www.rabbitmq.com/>`_ using `Pika <http://pika.readthedocs.org/en/latest/>`_ module. 

More precisly, this script collect instantaneous and historical data from Current Cost. It also take care of usb disconnection, Current Cost bad message format, timeout and power disconnection and send an error on stdout or on RabbitMQ each time for later anlysis. Also it create an udev rule to transform /dev/ttyUSB* to /dev/currentcost for serial port connection.

.. toctree::
    :maxdepth: 2

    presentation.rst
    code.rst
    todo.rst
    change.rst

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


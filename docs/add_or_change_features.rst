Add/Change Features
====================================


.. _parsers:

Parsers
------------

Adding a parser is easy:

1. Create a .py file with a name of your choice (just make sure it doesn't start with a _)

2. Contain your desired parsing logic in a function called 'parse' (the function may be a class method or not)

3. The 'parse' function receives a snapshot in a json format, and should return a json dictionary of the following format: {'user_id': <snapshots_user_id>, 'datetime': <snapshot's_datetime>, 'result': <parsers_name>, <parser_name>: <parser_result>}


4. Add a 'name' field to the function/class with the parser's name as value

5. Place the .py file in brain_freeze/parsers/parsers

That's it. Now when BrainFreeze starts it collects the parser, subscribes it to the snapshots topic and publishes
its results so they are saved in the database.

.. _mqs:

Message Queues
---------------

If you want to use a message queue different than the default (RabbitMQ), do the following:

1. Add the message queue's logic (functions to create, subscribe and publish to a topic) under a class in a .py file
2. Include that file in a directory under the utils directory
3. Open utils/message_queue_manager.py and add a <mq_name>:<class_name(from step 1)> item to the mqs dictionary

Next time you start BrainFreeze, pass the message queue's url to the server, parsers and saver.

.. _dbs:

Databases
------------

If you want to use a database different than the default (MongoDb), do the following:

1. Add the database's logic (functions to insert data to a table and retrieve it) under a class in a .py file
2. Include that file in a directory under the utils directory
3. Open utils/db_manager.py and add a <db_name>:<class_name(from step 1)> item to the dbs dictionary

Next time you start BrainFreeze, pass the database's url to the saver and API.


.. _logging:

Logger
------------

BrainFreeze uses python's logging module and slightly customizes.
If you want to use logging in one of your added modules (most modules of the system already use logging),
add the following lines to your module:
    >>> from ..utils import Logger # (or the appropriate path to the utils package)
    >>> logger = Logger(__name__).logger

A .log file will appear next to your module and have your logs in it the next time it is called.


.. image:: qo3vMue.png
  :target: https://i.imgur.com/qo3vMue.png
  :align: center
  :width: 200
  :alt: Moon
  :class: no-scaled-link
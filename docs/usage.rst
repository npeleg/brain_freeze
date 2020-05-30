.. _usage:

Usage
======

The **brain_freeze** package consists of the following components:


client
------

The client component is responsible for sending the user's information and cognition snapshots,
found in a binary file, to a server.
The reading of the binary file is done using a 'reader' component (see below).

Uploading the binary file to server is simple:
        >>> from brain_freeze.client import upload_sample
        >>> upload_sample(host= '127.0.0.1' , port= 8000 , path= './sample/sample.mind.gz' )
        uploading... # upload path to host : port


The client also provides a command-line interface::

        $ python -m brain_freeze.client upload-sample \
        -h/--host '127.0.0.1'                          \
        -p/--port 8000                                  \
        'sample/sample.mind.gz'



reader
--------

The reader handles the reading and parsing of the binary file containing the user's information
and cognition snapshots.

Uploading the binary file to server is simple:
        >>> from brain_freeze.client.reader import Reader
        >>> reader = Reader('sample/sample.mind.gz')
        >>> for snapshot in reader:
        ...    print(snapshot)


Or through a command-line interface::

        $ python -m brain_freeze.client.reader read 'sample/sample.mind.gz'

A sample file is available `here <https://storage.googleapis.com/advanced-system-design/sample.mind.gz>`_.



server
-------

The server receives user information and cognition snapshots, converts those to a suitable format
and forwards them to a message queue or just sends them to a user supplied function:

        >>> from brain_freeze.server import run_server
        >>> def print_message(message):
        ...    print(message)
        >>> run_server(host='127.0.0.1', port=8000, publish=print_message)
        ... # listen on host:port and pass received messages to publish
        >>> run_server(host='127.0.0.1', port=8000, publish='rabbitmq://127.0.0.1:5672/')
        ... # listen on host:port and pass received messages to rabbitmq


Command-line interface::

        $ python -m brain_freeze.server run-server \
        -h/--host '127.0.0.1'                       \
        -p/--port 8000                               \
        'rabbitmq://127.0.0.1:5672/'

The third argument is the message queue url.



parsers
---------

Parsers are simple functions or classes, consuming data (cognition snapshots) from the message queue,
processing that data and producing the parsed results back to the queue.
BrainFreeze currently supports parsing of a snapshot's pose, color image and feelings fields.

The parsers component consists of a "parsers logic" module that dynamically collects all the parsers
functions from a specific folder, subscribes them to the message queue so that snapshots are sent
to them and processed.

It is easy to add a parser of your choice - follow the instructions in the documentation. # TODO link

To run a specific parser on a "raw" snapshot and see
the parsed result (here we are running the pose parser):

        >>> from brain_freeze.parsers import parse
        >>> raw_snapshot = ...
        >>> result = parse('pose', raw_snapshot)


Or do it the CLI way (you can also specify a destination file to which the result will be saved)::

        $ python -m brain_freeze.parsers parse 'pose' 'snapshot.raw' > 'pose.result'


Results of pose and feelings parsers will be printed to the screen, while the color image result
will display the path of the saved file.

To subscribe a parser to the message queue run the following command::

        $ python -m brain_freeze.parsers run-parser 'pose' 'rabbitmq://127.0.0.1:5672/'


If you want to add a parser, go to :ref:`parsers` page.



saver
-----

The saver component is responsible for receiving parsed results of snapshots from the message queue
and saving them to a database.

You can save a single result:

        >>> from brain_freeze.saver import Saver
        >>> saver = Saver(database_url)
        >>> parsed_result = ...
        >>> saver.save('pose', parsed_result)

Or use the CLI::

        $ python -m brain_freeze.saver save        \
        -d/--database 'mongodb://127.0.0.1:27017' \
        'pose'                                      \
        'pose.result'

The third argument is a path to the file in which the result is stored.

Or run the saver as a service, so that it subscribes to all available parser topics,
and saves incoming parsed results to the database::

        $ python -m brain_freeze.saver run-saver  \
        'mongodb://127.0.0.1:27017'              \
        'rabbitmq://127.0.0.1:5672/'

The second argument is the database url and the third is the message queue url.



message queue
-------------

The project comes pre-packed with the RabbitMQ message queue service.
It starts running automatically upon the deployment of BrainFreeze.

The message queue has a topic for incoming snapshots from the server, to which all the parsers subscribe.
Each parser's results are published to a dedicated topic ('pose' topic for the pose parser, etc.),
and the saver subscribes to each of these topics.

If you want to change the message queue used in BrainFreeze, go to :ref:`mqs` page.



database
---------

The project comes pre-packed with the MongoDB database service, and uses it via pymongo.
It starts running automatically upon the deployment of BrainFreeze.

For the use of BrainFreeze, a single database named 'db' is created in MongoDB.
Inside it there are two collections: 'users' and 'snapshots'.
The users collection contains all the users information, and the snapshots collection stores
all the parsed results of all the users' snapshots (there is no internal partition in the
snapshots collection - every parsed result is inserted to the collection without any separation
according to user or timestamp).

If you want to change the message queue used in BrainFreeze, go to :ref:`dbs` page.



api
----

This component exposes the results saved in the database using REST.

To run the API server:

        >>> from brain_freeze.api import run_api_server
        >>> run_api_server(
        ...     host = '127.0.0.1',
        ...     port = 5000,
        ...     database_url = 'mongodb://127.0.0.1:27017'
        ... )
        ... # listen on host:port and serve data from database_url

Or use the CLI::

        $ python -m brain_freeze.api run-server \
        -h/--host '127.0.0.1'                  \
        -p/--port 5000                          \
        -d/--database 'mongodb://127.0.0.1:27017'

The API server supports the following RESTful API endpoints:

``GET /users``

Which returns the list of all the supported users, including their IDs and names.


``GET /users/user-id``

Which returns the specified user's details: ID, name, birthday and gender.


``GET /users/user-id/snapshots``

Which returns the list of the specified user's snapshot IDs and datetimes.


``GET /users/user-id/snapshots/snapshot-id``

Which returns the specified snapshot's details: ID, datetime, and the available results' names (e.g. pose).


``GET /users/user-id/snapshots/snapshot-id/result-name``

Which returns the specified snapshot's result.
Supported results are pose, color-image and feelings,
where color-image result will show the data's path, to be used to get the data:

``GET /users/user-id/snapshots/snapshot-id/color-image/path``



CLI
---

The CLI consumes the API and reflects its results.
(In every command "1" argument is the user id, "2" is a snapshots id and "pose" is the result.
All the commands accept the -h/--host and -p/--port flags to configure the host and port,
and default to the API's default address)::

    $ python -m brain_freeze.cli get-users
    …
    $ python -m brain_freeze.cli get-user 1
    …
    $ python -m brain_freeze.cli get-snapshots 1
    …
    $ python -m brain_freeze.cli get-snapshot 1 2
    …
    $ python -m brain_freeze.cli get-result 1 2 'pose'
    …

The get-result command also accepts the -s/--save flag that, if specified,
receives a path and saves the result's data to that path.



GUI
---

The GUI consumes the API and reflects it results.

To run the GUI server:
        >>> from brain_freeze.gui import run_server
        >>> run_server(
        ...     host = '127.0.0.1',
        ...     port = 8080,
        ...     api_host = '127.0.0.1',
        ...     api_port = 5000,
        ... )

Or use the CLI::

    $ python -m brain_freeze.gui run-server \
    -h/--host '127.0.0.1'                 \
    -p/--port 8080                         \
    -H/--api-host '127.0.0.1'               \
    -P/--api-port 5000


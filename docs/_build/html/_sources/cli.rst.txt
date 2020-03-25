asdF CLI Reference
====================

The ``asdF`` package provides a command-line interface:

.. code:: bash

    $ python -m asdF [COMMAND] [ARGS]
    ...


The ``upload_thought`` Command
-------------------------------

The ``upload_thought`` command sends the string THOUGHT of USER_ID to the server in ip and port ADDRESS:

.. code:: bash

    $ python -m asdF upload_thought [ADDRESS] [USER_ID] [THOUGHT]

The ``run_server`` Command
---------------------------

The ``run_server`` command opens a server at ip and port ADDRESS and stores thoguht from users at DATA_DIR:

.. code:: bash

    $ python -m asdF run_server [ADDRESS] [DATA_DIR]

The ``run_webserver`` Command
------------------------------

The run_webserver command serves the DATA_DIR directory on a server of ip and port ADDRESS:

.. code:: bash

    $ python -m asdF run_webserver [ADDRESS] [DATA_DIR]


.. brain_freeze documentation master file, created by
   sphinx-quickstart on Tue May 26 21:03:40 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


BrainFreeze
========================================

BrainFreeze is the software side of a computer-brain interface product.

The product's hardware side constantly produces cognition snapshots of a user,
sent to BrainFreeze system for processing and analysis.
A cognition snapshot is a structure which consists of:

- the user's **location** and head's **rotation** (combining those forms the user's **'pose'**)
- the **color image** that the user saw
- the **depth image** that the user saw (the distance of the nearest object in each point of the user's view)
- the **timestamp** the snapshot was taken at

To simulate the hardware side, a binary file is available for you (`here <https://storage.googleapis.com/advanced-system-design/sample.mind.gz>`_),
containing the user's basic information and a list of their cognition snapshots taken
in the morning hours of April 4th, 2019.

The software side, i.e. BrainFreeze system and its components, is further explained in the :ref:`usage` page.



Installation
------------

1. Clone the repository and enter it::

       $ git clone https://github.com/npeleg/brain_freeze.git
       ...
       $ cd brain_freeze/

2. Run the database and message queue::

       $ sudo docker run -d -p 27017:27017 mongo
       ...
       $ sudo docker run -d -p 5672:5672 rabbitmq
       ...

3. Install the virtual environment and enter it::

      $ scripts/install.sh
      ...
      $ source .env/bin/activate
      [brain_freeze] $


4. Run the pipeline script::

    $ scripts/run_pipeline.sh
    ...
    You're good to go!
    Start the client and see the results in your browser at localhost:8080



Proceed to other pages:

.. toctree::
   :maxdepth: 1

   usage
   add_or_change_features



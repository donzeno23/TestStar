Celery TestStar
=============

TestStar is based on Mher's Flower but extends the functionality to scheduled automated test suites
        
Features
--------
        
- Scheduled automated python test suites
        
    - Across multiple celery workers
    - Broker is RabbitMQ

- Real-time monitoring using Celery Events

    - Task progress and history
    - Ability to show task details (arguments, start time, runtime, and more)
    - Graphs and statistics

- Remote Control

    - View worker status and statistics
    - Shutdown and restart worker instances
    - Control worker pool size and autoscale settings
    - View and modify the queues a worker instance consumes from
    - View currently running tasks
    - View scheduled tasks (ETA/countdown)
    - View reserved and revoked tasks
    - Apply time and rate limits
    - Configuration viewer
    - Revoke or terminate tasks

- Broker monitoring

    - View statistics for all Celery queues
    - Queue length graphs

- HTTP API
- Basic Auth and Google OpenID authentication

API
---

Flower API enables to manage the cluster via REST api, call tasks and receive task
events in real-time via WebSockets.

For example you can schedule a deployment of packages: ::
        
    $ curl -X POST http://localhost:8888/api/deploy/package/myworker

Or you can restart worker's pool by: ::

    $ curl -X POST http://localhost:8888/api/worker/pool/restart/myworker

Or call a task by: ::

    $ curl -X POST -d '{"args":[1,2]}' http://localhost:8888/api/task/async-apply/tasks.add

Or terminate executing task by: ::

    $ curl -X POST -d 'terminate=True' http://localhost:8888/api/task/revoke/8a4da87b-e12b-4547-b89a-e92e4d1f8efd

Or receive task completion events in real-time: ::

    var ws = new WebSocket('ws://localhost:8888/api/task/events/task-succeeded/');
    ws.onmessage = function (event) {
        console.log(event.data);
    }

Installation
------------

To install, simply: ::

    $ pip install teststar

Usage
-----

Launch the server and open http://localhost:8888: ::

    $ teststar --port=5555

Or launch from celery: ::

    $ celery teststar --address=127.0.0.1 --port=8888

Broker URL and other configuration options can be passed through the standard Celery options: ::

    $ celery teststar --broker=amqp://guest:guest@localhost:5672//
    
    $ celery teststar --broker_url=amqp://guest:guest@localhost:5672// --broker_api=http://guest:guest@localhost:55672/api/

Screenshots
-----------

.. image:: https://raw.github.com/mdaloia/teststar/master/docs/screenshots/dashboard.png
   :width: 800px

.. image:: https://raw.github.com/mdaloia/teststar/master/docs/screenshots/pool.png
   :width: 800px

.. image:: https://raw.github.com/mdaloia/teststar/master/docs/screenshots/tasks.png
   :width: 800px

.. image:: https://raw.github.com/mdaloia/teststar/master/docs/screenshots/task.png
   :width: 800px

.. image:: https://raw.github.com/mdaloia/teststar/master/docs/screenshots/monitor.png
   :width: 800px

More screenshots_

.. _screenshots: https://github.com/mdaloia/teststar/tree/master/docs/screenshots

Getting help
------------

Please head over to #celery IRC channel on irc.freenode.net or
`open an issue`_.

.. _open an issue: https://github.com/mdaloia/teststar/issues


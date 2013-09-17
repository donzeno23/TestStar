To start teststar run the following from the command line:

C:\Users\mdaloia\TARTworkspace\TBWin\web\pyTB>python teststar --broker=amqp:// --broker_api=http://guest:guest@localhost:55672/api/

OR

C:\Users\mdaloia\TARTworkspace\TBWin\web\pyTB>python teststar --broker_url=amqp://guest:guest@localhost:5672// --broker_api=http://guest:guest@localhost:55672/api/

OR

C:\Users\mdaloia\TARTworkspace\TBWin\web\pyTB>celery --app=teststar --broker_url=amqp://guest:guest@localhost:5672// --broker_api=http://guest:guest@localhost:5
5672/api/

To send a task to Linux test agents:

TestStar log:

WorkerDeployPackage.post called
[I 130913 11:18:20 tasks:72] Starting task 'deploy-package' with '['deploy package', 'trunk', 'dir:core/be', 'mdaloia']' and '{u'suite_name': u'dir:core/be', u'
routing_key_name': u'trunk', u'job_name': u'run test suite'}' on 'nj1dvgtslnx01' worker
[I 130913 11:18:20 web:1635] 200 POST /api/worker/deploy/package/nj1dvgtslnx01 (::1) 83.00ms


celeryd log:

[2013-09-13 11:18:15,764: DEBUG/MainProcess] * Dump of currently registered tasks:
celery.backend_cleanup
celery.chain
celery.chord
celery.chord_unlock
celery.chunks
celery.group
celery.map
celery.starmap
tasks.DeployPackage
tasks.RunPackage
tasks.SumTask
[2013-09-13 11:18:16,622: DEBUG/MainProcess] --Empty queue--
[2013-09-13 11:18:16,776: DEBUG/MainProcess] * Dump of current schedule:
0. 2013-09-13 15:18:20.605362 pri0 <TimerEntry: maintain_pool(*[], **{})
1. 2013-09-13 15:18:20.605642 pri0 <TimerEntry: _send(*('worker-heartbeat',), **{})
[2013-09-13 11:18:18,797: DEBUG/MainProcess] --Empty queue--
[2013-09-13 11:18:20,327: INFO/MainProcess] Got task from broker: tasks.DeployPackage[deploy-package-da3b8303-5871-4922-aa7f-b4bce3e58ed3]
[2013-09-13 11:18:20,344: DEBUG/MainProcess] Mediator: Running callback for task: tasks.DeployPackage[deploy-package-da3b8303-5871-4922-aa7f-b4bce3e58ed3]
[2013-09-13 11:18:20,345: DEBUG/MainProcess] TaskPool: Apply <function _fast_trace_task at 0x1e09e2a8> (args:('tasks.DeployPackage', 'deploy-package-da3b8303-5871-4922-aa7f-b4bce3e58ed3', ['deploy package', u'testbench.nj1dvgtslnx01', 'dir:core/be', 'mdaloia'], {u'routing_key_name': u'trunk', u'suite_name': u'dir:core/be', u'job_name': u'run test suite'}, {'utc': True, 'is_eager': False, 'chord': None, 'group': None, 'args': ['deploy package', u'testbench.nj1dvgtslnx01', 'dir:core/be', 'mdaloia'], 'retries': 0, 'delivery_info': {'priority': None, 'routing_key': 'testbench.nj1dvgtslnx01', 'exchange': 'testbench'}, 'expires': None, 'task': 'tasks.DeployPackage', 'callbacks': None, 'errbacks': None, 'hostname': 'nj1dvgtslnx01', 'taskset': None, 'kwargs': {u'routing_key_name': u'trunk', u'suite_name': u'dir:core/be', u'job_name': u'run test suite'}, 'eta': None, 'id': 'deploy-package-da3b8303-5871-4922-aa7f-b4bce3e58ed3'}) kwargs:{})
[2013-09-13 11:18:20,346: DEBUG/MainProcess] Task accepted: tasks.DeployPackage[deploy-package-da3b8303-5871-4922-aa7f-b4bce3e58ed3] pid:18341
[2013-09-13 11:18:20,346: INFO/MainProcess] tasks.DeployPackage[deploy-package-da3b8303-5871-4922-aa7f-b4bce3e58ed3]: Start deploying package for spec: testbench.nj1dvgtslnx01
[2013-09-13 11:18:20,382: INFO/PoolWorker-1] Starting new HTTP connection (1): atsbuildserver
[2013-09-13 11:18:20,388: DEBUG/PoolWorker-1] "GET /guestAuth/repository/download/package_PackageBootstrap/latest.lastSuccessful/PackageBootstrap.zip HTTP/1.1" 200 5229902
[2013-09-13 11:18:20,421: ERROR/MainProcess] tasks.DeployPackage[deploy-package-da3b8303-5871-4922-aa7f-b4bce3e58ed3]: Platform 'linux2' is not supported
[2013-09-13 11:18:20,444: INFO/MainProcess] tasks.DeployPackage[deploy-package-da3b8303-5871-4922-aa7f-b4bce3e58ed3]: Task - DeployPackage - success
[2013-09-13 11:18:20,444: INFO/MainProcess] Task tasks.DeployPackage[deploy-package-da3b8303-5871-4922-aa7f-b4bce3e58ed3] succeeded in 0.0991489887238s: 'Deploy Package succeeded'

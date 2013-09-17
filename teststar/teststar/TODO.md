[I 130912 16:24:14 web:1635] 304 GET /static/js/teststar.js?v=02e38b9956ac153ec8b05826d3eef0f5 (::1) 1.00ms
BaseHandler - prepare
dir-self.application:  ['__call__', '__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__','__repr__','__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_get_host_handlers', '_load_ui_methods', '_load_ui_modules', '_wsgi', 'add_handlers', 'add_transform', 'auth','basic_auth', 'broker_api', 'celery_app', 'default_host', 'events', 'handlers','io_loop', 'listen', 'log_request', 'named_handlers', 'options', 'reverse_url', 'settings', 'ssl', 'start', 'state', 'stop','transforms', 'ui_methods', 'ui_modules']
BaseHandler - get_current_user
WorkerDeployPackage.post called
[I 130912 16:24:19 control:28] Starting deploy package on 'nj1dvgtslnx01' worker
teststar.control-Response:  [{u'nj1dvgtslnx01': {u'error': u"KeyError(u'python package.py',)"}}]
[E 130912 16:24:19 control:41] [{u'nj1dvgtslnx01': {u'error': u"KeyError(u'python package.py',)"}}]
[W 130912 16:24:19 web:1635] 403 POST /api/worker/deploy/package/nj1dvgtslnx01 (::1) 146.00ms

#TODO: need to define json data in teststar.js in function ???

WorkerDeployPackage.post called
[E 130912 17:36:58 web:1228] Uncaught exception POST /api/worker/deploy/package/nj1dvgtslnx01 (::1)
    HTTPRequest(protocol='http', host='localhost:8888', method='POST', uri='/api/worker/deploy/package/nj1dvgtslnx01', version='HTTP/1.1', remote_ip='::1', headers={'Origin': 'http://localhost:8888', 'Content-Length': '24', 'Accept-Language': 'en-US,en;q=0.8', 'Accept-Encoding': 'gzip,deflate,sdch', 'Host': 'localhost:8888', 'Accept': 'application/json, text/javascript, */*; q=0.01', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36', 'Connection': 'keep-alive', 'X-Requested-With': 'XMLHttpRequest', 'Referer': 'http://localhost:8888/workers', 'Cookie': 'csrftoken=QTb2tp6sRT6Bra8wEoQqJknztq2VeSJm; m=6967:t|34e2:|47ba:t|2d14:f|6cfc:t|15cc:t|77cb:t|5be5:t|2a03:t|ca3:t|54e1:t|4a01:t', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'})
    Traceback (most recent call last):
      File "C:\Python27\lib\site-packages\tornado\web.py", line 1141, in _when_complete
        callback()
      File "C:\Python27\lib\site-packages\tornado\web.py", line 1162, in _execute_method
        self._when_complete(method(*self.path_args, **self.path_kwargs),
      File "C:\Python27\lib\site-packages\tornado\web.py", line 2293, in wrapper
        return method(self, *args, **kwargs)
      File "teststar\api\tasks.py", line 49, in post
        args, kwargs, options = self.get_task_args()
      File "teststar\api\tasks.py", line 21, in get_task_args
        options = json_decode(self.request.body)
      File "C:\Python27\lib\site-packages\tornado\escape.py", line 83, in json_decode
        return json.loads(to_basestring(value))
      File "C:\Python27\lib\json\__init__.py", line 326, in loads
        return _default_decoder.decode(s)
      File "C:\Python27\lib\json\decoder.py", line 366, in decode
        obj, end = self.raw_decode(s, idx=_w(s, 0).end())
      File "C:\Python27\lib\json\decoder.py", line 384, in raw_decode
        raise ValueError("No JSON object could be decoded")
    ValueError: No JSON object could be decoded
[E 130912 17:36:59 web:1635] 500 POST /api/worker/deploy/package/nj1dvgtslnx01 (::1) 232.00ms


send_task

WorkerDeployPackage.post called
[I 130912 17:40:13 tasks:61] Starting task 'deploy-package' with '['deploy package', 'trunk', 'dir:core/be', 'mdaloia']' and '{u'suite_name': u'dir:core/be', u'routing_key_name': u'trunk', u'job_name': u'run test suite'}' on 'nj1dvgtslnx01' worker
[I 130912 17:40:13 web:1635] 200 POST /api/worker/deploy/package/nj1dvgtslnx01 (::1) 123.00ms


apply_async

WorkerDeployPackage.post called
[I 130912 17:55:28 tasks:66] Starting task 'deploy-package' with '['deploy package', 'trunk', 'dir:core/be', 'mdaloia']' and '{u'suite_name': u'dir:core/be', u'
routing_key_name': u'trunk', u'job_name': u'run test suite'}' on 'nj1dvgtslnx01' worker
[I 130912 17:55:28 web:1635] 200 POST /api/worker/deploy/package/nj1dvgtslnx01 (::1) 108.00ms


received unregistered task

[2013-09-13 10:14:38,397: ERROR/MainProcess] Received unregistered task of type 'test_bench.tasks.DeployPackage'.
The message has been ignored and discarded.

Did you remember to import the module containing this task?
Or maybe you are using relative imports?
More: http://docs.celeryq.org/en/latest/userguide/tasks.html#names

The full contents of the message body was:
{'utc': True, 'chord': None, 'args': ['deploy package', u'testbench.nj1dvgtslnx01', 'dir:core/be', 'mdaloia'], 'retries': 0, 'expires': None, 'task': 'test_bench.tasks.DeployPackage', 'callbacks': None, 'errbacks': None, 'taskset': None, 'kwargs': {u'routing_key_name': u'trunk', u'suite_name': u'dir:core/be', u'job_name': u'run test suite'}, 'eta': None, 'id': 'deploy-package-899f58cf-b62e-4769-bf00-34ed8f3155fb'} (409b)
Traceback (most recent call last):
  File "/home/mdaloia/local/Python-2.6.8/lib/python2.6/site-packages/celery/worker/consumer.py", line 453, in on_task_received
    strategies[name](message, body, message.ack_log_error)
KeyError: 'test_bench.tasks.DeployPackage'
[2013-09-13 10:14:40,610: DEBUG/MainProcess] * Dump of currently registered tasks:
celery.backend_cleanup
celery.chain
celery.chord
celery.chord_unlock
celery.chunks
celery.group
celery.map
celery.starmap
tasks.RunPackage
tasks.SumTask

Using apply_async

Change on server - teststar/tasks.py and agent - /home/mdaloia/tasks.py
@task(base=DeployPackage, name="tasks.DeployPackage")

[2013-09-13 10:32:46,589: DEBUG/MainProcess] * Dump of currently registered tasks:
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
[2013-09-13 10:32:46,867: DEBUG/MainProcess] * Dump of current schedule:
0. 2013-09-13 14:32:48.542457 pri0 <TimerEntry: _send(*('worker-heartbeat',), **{})
1. 2013-09-13 14:32:49.559344 pri0 <TimerEntry: maintain_pool(*[], **{})
[2013-09-13 10:32:47,603: DEBUG/MainProcess] * Dump of current schedule:
0. 2013-09-13 14:32:48.542457 pri0 <TimerEntry: _send(*('worker-heartbeat',), **{})
1. 2013-09-13 14:32:49.559344 pri0 <TimerEntry: maintain_pool(*[], **{})
[2013-09-13 10:32:48,896: DEBUG/MainProcess] --Empty queue--
[2013-09-13 10:32:49,632: DEBUG/MainProcess] --Empty queue--
[2013-09-13 10:32:51,363: INFO/MainProcess] Got task from broker: tasks.DeployPackage[deploy-package-672c176f-492b-4c55-9c48-1b7b5d2a7e00]
[2013-09-13 10:32:51,392: DEBUG/MainProcess] Mediator: Running callback for task: tasks.DeployPackage[deploy-package-672c176f-492b-4c55-9c48-1b7b5d2a7e00]
[2013-09-13 10:32:51,392: DEBUG/MainProcess] TaskPool: Apply <function _fast_trace_task at 0x1779a2a8> (args:('tasks.DeployPackage', 'deploy-package-672c176f-492b-4c55-9c48-1b7b5d2a7e00', ['deploy package', u'testbench.nj1dvgtslnx01', 'dir:core/be', 'mdaloia'], {u'routing_key_name': u'trunk', u'suite_name': u'dir:core/be', u'job_name': u'run test suite'}, {'utc': True, 'is_eager': False, 'chord': None, 'group': None, 'args': ['deploy package', u'testbench.nj1dvgtslnx01', 'dir:core/be', 'mdaloia'], 'retries': 0, 'delivery_info': {'priority': None, 'routing_key': 'testbench.nj1dvgtslnx01', 'exchange': 'testbench'}, 'expires': None, 'task': 'tasks.DeployPackage', 'callbacks': None, 'errbacks': None, 'hostname': 'nj1dvgtslnx01', 'taskset': None, 'kwargs': {u'routing_key_name': u'trunk', u'suite_name': u'dir:core/be', u'job_name': u'run test suite'}, 'eta': None, 'id': 'deploy-package-672c176f-492b-4c55-9c48-1b7b5d2a7e00'}) kwargs:{})
[2013-09-13 10:32:51,395: DEBUG/MainProcess] Task accepted: tasks.DeployPackage[deploy-package-672c176f-492b-4c55-9c48-1b7b5d2a7e00] pid:18105
[2013-09-13 10:32:51,428: WARNING/PoolWorker-1] /home/mdaloia/local/Python-2.6.8/lib/python2.6/site-packages/celery/task/trace.py:341: RuntimeWarning: Exception raised outside body: NameError("global name 'logger' is not defined",):
Traceback (most recent call last):
  File "/home/mdaloia/local/Python-2.6.8/lib/python2.6/site-packages/celery/task/trace.py", line 247, in trace_task
    R = I.handle_error_state(task, eager=eager)
  File "/home/mdaloia/local/Python-2.6.8/lib/python2.6/site-packages/celery/task/trace.py", line 108, in handle_error_state
    }[self.state](task, store_errors=store_errors)
  File "/home/mdaloia/local/Python-2.6.8/lib/python2.6/site-packages/celery/task/trace.py", line 139, in handle_failure
    task.on_failure(exc, req.id, req.args, req.kwargs, einfo)
  File "/home/mdaloia/tasks.py", line 29, in on_failure
    logger.info("Task - DeployPackage - failure")
NameError: global name 'logger' is not defined

  exc, exc_info.traceback)))
[2013-09-13 10:32:51,430: CRITICAL/MainProcess] Task tasks.DeployPackage[deploy-package-672c176f-492b-4c55-9c48-1b7b5d2a7e00] INTERNAL ERROR: NameError("global name 'logger' is not defined",)
Traceback (most recent call last):
  File "/home/mdaloia/local/Python-2.6.8/lib/python2.6/site-packages/celery/task/trace.py", line 247, in trace_task
    R = I.handle_error_state(task, eager=eager)
  File "/home/mdaloia/local/Python-2.6.8/lib/python2.6/site-packages/celery/task/trace.py", line 108, in handle_error_state
    }[self.state](task, store_errors=store_errors)
  File "/home/mdaloia/local/Python-2.6.8/lib/python2.6/site-packages/celery/task/trace.py", line 139, in handle_failure
    task.on_failure(exc, req.id, req.args, req.kwargs, einfo)
  File "/home/mdaloia/tasks.py", line 29, in on_failure
    logger.info("Task - DeployPackage - failure")
NameError: global name 'logger' is not defined

Above issue was fixed with import logger from celery.utils.log import get_task_logger and logger=get_task_logger(__name__)

Also need to install cx_Oracle on nj1dvgtslnx01

[mdaloia@nj1dvgtslnx01 ~]$ pip install cx_Oracle
Downloading/unpacking cx-Oracle
  Running setup.py egg_info for package cx-Oracle
    Traceback (most recent call last):
      File "<string>", line 14, in <module>
      File "/home/mdaloia/build/cx-Oracle/setup.py", line 126, in <module>
        raise DistutilsSetupError(messageFormat % userOracleHome)
    distutils.errors.DistutilsSetupError: Oracle home (/appdata/u00/app/oracle/product/11.2.0/client_1) does not refer to an 9i, 10g or 11g installation.
    Complete output from command python setup.py egg_info:
    Traceback (most recent call last):

  File "<string>", line 14, in <module>

  File "/home/mdaloia/build/cx-Oracle/setup.py", line 126, in <module>

    raise DistutilsSetupError(messageFormat % userOracleHome)

distutils.errors.DistutilsSetupError: Oracle home (/appdata/u00/app/oracle/product/11.2.0/client_1) does not refer to an 9i, 10g or 11g installation.

----------------------------------------
Command python setup.py egg_info failed with error code 1 in /home/mdaloia/build/cx-Oracle
Storing complete log in /home/mdaloia/.pip/pip.log


However, 11g isn't installed, only 10g

export ORACLE_HOME=/appdata/u00/app/oracle/product/10.2.0/client_1

pip install cx_Oracle

(See below)

[mdaloia@nj1dvgtslnx01 ~]$ echo $ORACLE_HOME
/appdata/u00/app/oracle/product/11.2.0/client_1
[mdaloia@nj1dvgtslnx01 ~]$ export ORACLE_HOME=/appdata/u00/app/oracle/product/10.2.0/client_1
[mdaloia@nj1dvgtslnx01 ~]$ echo $ORACLE_HOME
/appdata/u00/app/oracle/product/10.2.0/client_1
[mdaloia@nj1dvgtslnx01 ~]$ pip install cx_Oracle
Downloading/unpacking cx-Oracle
  Running setup.py egg_info for package cx-Oracle
Installing collected packages: cx-Oracle
  Running setup.py install for cx-Oracle
    building 'cx_Oracle' extension
    gcc -pthread -fno-strict-aliasing -g -O2 -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes -fPIC -I/appdata/u00/app/oracle/product/10.2.0/client_1/rdbms/demo -I/appdata/u00/app/oracle/product/10.2.0/client_1/rdbms/public -I/home/mdaloia/local/Python-2.6.8/include/python2.6 -c cx_Oracle.c -o build/temp.linux-x86_64-2.6-10g/cx_Oracle.o -DBUILD_VERSION=5.1.2
    In file included from /appdata/u00/app/oracle/product/10.2.0/client_1/rdbms/public/oci.h:2681,
                     from cx_Oracle.c:10:
    /appdata/u00/app/oracle/product/10.2.0/client_1/rdbms/public/oci1.h:148: warning: function declaration isnât a prototype
    In file included from /appdata/u00/app/oracle/product/10.2.0/client_1/rdbms/public/ociap.h:230,
                     from /appdata/u00/app/oracle/product/10.2.0/client_1/rdbms/public/oci.h:2705,
                     from cx_Oracle.c:10:
    /appdata/u00/app/oracle/product/10.2.0/client_1/rdbms/public/nzt.h:676: warning: function declaration isnât a prototype
    /appdata/u00/app/oracle/product/10.2.0/client_1/rdbms/public/nzt.h:2667: warning: function declaration isnât a prototype
    /appdata/u00/app/oracle/product/10.2.0/client_1/rdbms/public/nzt.h:2676: warning: function declaration isnât a prototype
    /appdata/u00/app/oracle/product/10.2.0/client_1/rdbms/public/nzt.h:2686: warning: function declaration isnât a prototype
    /appdata/u00/app/oracle/product/10.2.0/client_1/rdbms/public/nzt.h:2695: warning: function declaration isnât a prototype
    /appdata/u00/app/oracle/product/10.2.0/client_1/rdbms/public/nzt.h:2704: warning: function declaration isnât a prototype
    /appdata/u00/app/oracle/product/10.2.0/client_1/rdbms/public/nzt.h:2713: warning: function declaration isnât a prototype
    /appdata/u00/app/oracle/product/10.2.0/client_1/rdbms/public/nzt.h:2721: warning: function declaration isnât a prototype
    /appdata/u00/app/oracle/product/10.2.0/client_1/rdbms/public/nzt.h:2731: warning: function declaration isnât a prototype
    /appdata/u00/app/oracle/product/10.2.0/client_1/rdbms/public/nzt.h:2738: warning: function declaration isnât a prototype
    /appdata/u00/app/oracle/product/10.2.0/client_1/rdbms/public/nzt.h:2746: warning: function declaration isnât a prototype
    In file included from /appdata/u00/app/oracle/product/10.2.0/client_1/rdbms/public/oci.h:2705,
                     from cx_Oracle.c:10:
    /appdata/u00/app/oracle/product/10.2.0/client_1/rdbms/public/ociap.h:10077: warning: function declaration isnât a prototype
    /appdata/u00/app/oracle/product/10.2.0/client_1/rdbms/public/ociap.h:10083: warning: function declaration isnât a prototype
    gcc -pthread -shared build/temp.linux-x86_64-2.6-10g/cx_Oracle.o -L/appdata/u00/app/oracle/product/10.2.0/client_1/lib -lclntsh -o build/lib.linux-x86_64-2.6-10g/cx_Oracle.so
Successfully installed cx-Oracle
Cleaning up...
[mdaloia@nj1dvgtslnx01 ~]$ python
Python 2.6.8 (unknown, Aug  2 2012, 12:07:26)
[GCC 4.1.2 20080704 (Red Hat 4.1.2-48)] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import cx_Oracle


echo $ORACLE_HOME
/appdata/u00/app/oracle/product/11.2.0/client_1



Issue:

[2013-09-13 10:59:41,815: DEBUG/MainProcess] * Dump of currently registered tasks:
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
[2013-09-13 10:59:42,744: INFO/MainProcess] Got task from broker: tasks.DeployPackage[deploy-package-3d272d01-a9f4-46d4-9fd2-f8f60760136a]
[2013-09-13 10:59:42,779: DEBUG/MainProcess] Mediator: Running callback for task: tasks.DeployPackage[deploy-package-3d272d01-a9f4-46d4-9fd2-f8f60760136a]
[2013-09-13 10:59:42,780: DEBUG/MainProcess] TaskPool: Apply <function _fast_trace_task at 0x1c7242a8> (args:('tasks.DeployPackage', 'deploy-package-3d272d01-a9f4-46d4-9fd2-f8f60760136a', ['deploy package', u'testbench.nj1dvgtslnx01', 'dir:core/be', 'mdaloia'], {u'routing_key_name': u'trunk', u'suite_name': u'dir:core/be', u'job_name': u'run test suite'}, {'utc': True, 'is_eager': False, 'chord': None, 'group': None, 'args': ['deploy package', u'testbench.nj1dvgtslnx01', 'dir:core/be', 'mdaloia'], 'retries': 0, 'delivery_info': {'priority': None, 'routing_key': 'testbench.nj1dvgtslnx01', 'exchange': 'testbench'}, 'expires': None, 'task': 'tasks.DeployPackage', 'callbacks': None, 'errbacks': None, 'hostname': 'nj1dvgtslnx01', 'taskset': None, 'kwargs': {u'routing_key_name': u'trunk', u'suite_name': u'dir:core/be', u'job_name': u'run test suite'}, 'eta': None, 'id': 'deploy-package-3d272d01-a9f4-46d4-9fd2-f8f60760136a'}) kwargs:{})
[2013-09-13 10:59:42,780: INFO/MainProcess] tasks.DeployPackage[deploy-package-3d272d01-a9f4-46d4-9fd2-f8f60760136a]: Start deploying package for spec: testbench.nj1dvgtslnx01
[2013-09-13 10:59:42,786: DEBUG/MainProcess] Task accepted: tasks.DeployPackage[deploy-package-3d272d01-a9f4-46d4-9fd2-f8f60760136a] pid:18233
[2013-09-13 10:59:42,827: DEBUG/MainProcess] * Dump of current schedule:
0. 2013-09-13 14:59:43.770914 pri0 <TimerEntry: maintain_pool(*[], **{})
1. 2013-09-13 14:59:44.785024 pri0 <TimerEntry: _send(*('worker-heartbeat',), **{})
[2013-09-13 10:59:42,833: INFO/MainProcess] tasks.DeployPackage[deploy-package-3d272d01-a9f4-46d4-9fd2-f8f60760136a]: Task - DeployPackage - failure
[2013-09-13 10:59:42,834: ERROR/MainProcess] Task tasks.DeployPackage[deploy-package-3d272d01-a9f4-46d4-9fd2-f8f60760136a] raised exception: ImportError('No module named requests',)
Traceback (most recent call last):
  File "/home/mdaloia/local/Python-2.6.8/lib/python2.6/site-packages/celery/task/trace.py", line 233, in trace_task
    R = retval = fun(*args, **kwargs)
  File "/home/mdaloia/local/Python-2.6.8/lib/python2.6/site-packages/celery/task/trace.py", line 420, in __protected_call__
    return self.run(*args, **kwargs)
  File "/home/mdaloia/tasks.py", line 54, in deploy_package
    import requests
None: No module named requests
[2013-09-13 10:59:44,853: DEBUG/MainProcess] --Empty queue--


Solution:
[mdaloia@nj1dvgtslnx01 ~]$ pip install requests
Downloading/unpacking requests
  Downloading requests-1.2.3.tar.gz (348Kb): 348Kb downloaded
  Running setup.py egg_info for package requests
Installing collected packages: requests
  Running setup.py install for requests
Successfully installed requests
Cleaning up...


Looks like deploy package task worked!!!

[2013-09-13 11:04:33,929: DEBUG/MainProcess] * Dump of currently registered tasks:
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
[2013-09-13 11:04:34,942: DEBUG/MainProcess] * Dump of current schedule:
0. 2013-09-13 15:04:37.180616 pri0 <TimerEntry: maintain_pool(*[], **{})
1. 2013-09-13 15:04:37.180943 pri0 <TimerEntry: _send(*('worker-heartbeat',), **{})
[2013-09-13 11:04:35,281: DEBUG/MainProcess] --Empty queue--
[2013-09-13 11:04:36,969: DEBUG/MainProcess] --Empty queue--
[2013-09-13 11:04:39,352: INFO/MainProcess] Got task from broker: tasks.DeployPackage[deploy-package-7e59198d-0cc0-4fec-9a9f-53d79c3cf148]
[2013-09-13 11:04:39,374: DEBUG/MainProcess] Mediator: Running callback for task: tasks.DeployPackage[deploy-package-7e59198d-0cc0-4fec-9a9f-53d79c3cf148]
[2013-09-13 11:04:39,374: DEBUG/MainProcess] TaskPool: Apply <function _fast_trace_task at 0x1c7242a8> (args:('tasks.DeployPackage', 'deploy-package-7e59198d-0cc0-4fec-9a9f-53d79c3cf148', ['deploy package', u'testbench.nj1dvgtslnx01', 'dir:core/be', 'mdaloia'], {u'routing_key_name': u'trunk', u'suite_name': u'dir:core/be', u'job_name': u'run test suite'}, {'utc': True, 'is_eager': False, 'chord': None, 'group': None, 'args': ['deploy package', u'testbench.nj1dvgtslnx01', 'dir:core/be', 'mdaloia'], 'retries': 0, 'delivery_info': {'priority': None, 'routing_key': 'testbench.nj1dvgtslnx01', 'exchange': 'testbench'}, 'expires': None, 'task': 'tasks.DeployPackage', 'callbacks': None, 'errbacks': None, 'hostname': 'nj1dvgtslnx01', 'taskset': None, 'kwargs': {u'routing_key_name': u'trunk', u'suite_name': u'dir:core/be', u'job_name': u'run test suite'}, 'eta': None, 'id': 'deploy-package-7e59198d-0cc0-4fec-9a9f-53d79c3cf148'}) kwargs:{})
[2013-09-13 11:04:39,375: INFO/MainProcess] tasks.DeployPackage[deploy-package-7e59198d-0cc0-4fec-9a9f-53d79c3cf148]: Start deploying package for spec: testbench.nj1dvgtslnx01
[2013-09-13 11:04:39,384: DEBUG/MainProcess] Task accepted: tasks.DeployPackage[deploy-package-7e59198d-0cc0-4fec-9a9f-53d79c3cf148] pid:18233
[2013-09-13 11:04:39,459: INFO/PoolWorker-1] Starting new HTTP connection (1): atsbuildserver
[2013-09-13 11:04:39,477: DEBUG/PoolWorker-1] "GET /guestAuth/repository/download/package_PackageBootstrap/latest.lastSuccessful/PackageBootstrap.zip HTTP/1.1" 200 5229712
[2013-09-13 11:04:39,628: INFO/MainProcess] tasks.DeployPackage[deploy-package-7e59198d-0cc0-4fec-9a9f-53d79c3cf148]: Task - DeployPackage - success
[2013-09-13 11:04:39,629: INFO/MainProcess] Task tasks.DeployPackage[deploy-package-7e59198d-0cc0-4fec-9a9f-53d79c3cf148] succeeded in 0.253736019135s: 'Deploy Package succeeded'
[2013-09-13 11:04:42,395: DEBUG/MainProcess] * Dump of currently registered tasks:
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


Control Task - Restarting the worker pool

[I 130913 11:29:32 control:71] Restarting 'nj1dvgtslnx01' worker's pool
teststar.control-Response:  [{u'nj1dvgtslnx01': {u'ok': u'reload started'}}]
[I 130913 11:29:32 web:1635] 200 POST /api/worker/pool/restart/nj1dvgtslnx01 (::1) 83.00ms

Success! Restarting 'nj1dvgtslnx01' worker's pool



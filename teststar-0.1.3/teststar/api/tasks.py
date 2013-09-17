from __future__ import absolute_import

import json
import logging

from tornado import web
from tornado.escape import json_decode
from tornado.web import HTTPError

from celery import states
from celery.result import AsyncResult
from celery.backends.base import DisabledBackend
from celery.utils import gen_unique_id

from ..models import TaskModel, WorkersModel, Suite, SuiteError, TestRun, TestError
#NOTE: the below is used when running python teststar ...
#from models import TaskModel, WorkersModel, Suite, SuiteError, TestRun, TestError
from django.db import connection
from django.db import transaction
from django.db.models import Q
from django.db.models import Max, Min, Count


from ..views import BaseHandler
#NOTE: the below is used when running python teststar ...
#from views import BaseHandler

from .. import tasks
#NOTE: the below is used when running python teststar ...
#import tasks

class BaseTaskHandler(BaseHandler):
    def get_task_args(self):
        options = json_decode(self.request.body)
        args = options.pop('args', [])
        kwargs = options.pop('kwargs', {})
        return args, kwargs, options

    def is_worker(self, name):
        return WorkersModel.is_worker(self.application, name)

    @staticmethod
    def backend_configured(result):
        return not isinstance(result.backend, DisabledBackend)

    def write_error(self, status_code, **kwargs):
        self.set_status(status_code)


class WorkerDeployPackage(BaseTaskHandler):
    logging.debug("Calling WorkerDeployPackage")
    
    @web.authenticated
    def post(self, workername):
        if not self.is_worker(workername):
            raise web.HTTPError(404, "Unknown worker '%s'" % workername)
        celery = self.application.celery_app
        
        ###############################
        #TODO: uncomment once json objects added to teststar.js
        ####args, kwargs, options = self.get_task_args() 
        taskname = 'deploy-package'

        #TODO: temporarily hard-code args and kwargs
        name = 'deploy package'
        routing_key = 'trunk'
        suite = 'dir:core/be'
        owner = 'mdaloia'
        args = [name, routing_key, suite, owner]
        #task_id = "deploy-package-"+gen_unique_id()
        task_id = taskname+"-"+gen_unique_id()
        kwargs = {u'routing_key_name': u'trunk', u'suite_name': u'dir:core/be', u'job_name': u'run test suite'}
        exchange = 'testbench'
        routing_key = 'testbench.'+workername

        logging.info("Starting task '%s' with '%s' and '%s' on '%s' worker" % (taskname, args, kwargs, workername))
        
        ##deploy_result = celery.send_task(taskname, args=args, kwargs=kwargs)
        deploy_result = tasks.deploy_package.apply_async(args=[name, routing_key, suite, owner], 
                                                         task_id=taskname+"-"+gen_unique_id(),
                                                         kwargs={u'routing_key_name': u'trunk', u'suite_name': u'dir:core/be', u'job_name': u'run test suite'},
                                                         exchange='testbench',
                                                         routing_key="testbench."+workername)
        
        response = {'task-id': deploy_result.task_id}
        logging.info("Deploy Package response '%s' " % response) #'{'task-id': 'deploy-package-fa77046d-67bf-4d32-914c-5523983a9641'}'
        if self.backend_configured(deploy_result):
            response.update(state=deploy_result.state)
        logging.info("Deploy Package updated response '%s' " % response) #'{'task-id': 'deploy-package-fa77046d-67bf-4d32-914c-5523983a9641'}'
        logging.info("Deploy Package state '%s' " % deploy_result.state) 
        self.write(response)        
        
        #if response and 'ok' in response[0][workername]:
        #    self.write(dict(
        #        message="Deploying package to '%s' worker" % workername))
        #else:
        #    logging.error(response)
        #    self.set_status(403)
        #    self.write("Failed to deploy package to the '%s' worker" % workername)
        ################################
                
        '''
        if response and 'ok' in response[0][workername]:
            self.write(dict(
                message="Deploying package to '%s' worker" % workername))
        else:
            logging.error(response)
            self.set_status(403)
            self.write("Failed to deploy package to the '%s' worker" % workername)
        '''

#class WorkerRunPackage(BaseTaskHandler): pass
class WorkerDeployAndRunPackage(BaseTaskHandler): pass
class WorkerDeployAndRunPackage(BaseTaskHandler): pass
#class WorkerCreateDB(BaseTaskHandler): pass
class WorkerRunTestSuite(BaseTaskHandler): pass
class WorkerRunFailedTestSuite(BaseTaskHandler): pass


class TaskAsyncApply(BaseTaskHandler):
    @web.authenticated
    def post(self, taskname):
        celery = self.application.celery_app

        args, kwargs, options = self.get_task_args()
        logging.debug("Invoking task '%s' with '%s' and '%s'" %
                     (taskname, args, kwargs))
        result = celery.send_task(taskname, args=args, kwargs=kwargs)
        response = {'task-id': result.task_id}
        if self.backend_configured(result):
            response.update(state=result.state)
        self.write(response)


class TaskResult(BaseTaskHandler):
    @web.authenticated
    def get(self, taskid):
        result = AsyncResult(taskid)
        if not self.backend_configured(result):
            raise HTTPError(503)
        response = {'task-id': taskid, 'state': result.state}
        if result.ready():
            if result.state == states.FAILURE:
                response.update({'result': self.safe_result(result.result),
                                 'traceback': result.traceback})
            else:
                response.update({'result': self.safe_result(result.result)})
        self.write(response)

    def safe_result(self, result):
        "returns json encodable result"
        try:
            json.dumps(result)
        except TypeError:
            return repr(result)
        else:
            return result



class ListTasks(BaseTaskHandler):
    @web.authenticated
    def get(self):
        app = self.application
        limit = self.get_argument('limit', None)
        worker = self.get_argument('worker', None)
        type = self.get_argument('type', None)
        state = self.get_argument('state', None)

        limit = limit and int(limit)
        worker = worker if worker != 'All' else None
        type = type if type != 'All' else None
        state = state if state != 'All' else None

        tasks = {}
        for (id, task) in TaskModel.iter_tasks(app, limit=limit, type=type,
                                               worker=worker, state=state):
            tasks[id] = task

        self.write(tasks)

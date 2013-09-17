'''
Notes: See http://docs.celeryproject.org/en/latest/faq.html

Should I use retry or acks_late?

Task.retry is used to retry tasks, notably for expected errors that is catchable with the try: block
The AMQP (aka rabbitmq) transaction is not used for these errors: if the task raises an exception it is still acknowledged!

Can I schedule tasks to execute at a specific time?

You can use the eta argument of Task.apply_async()

Or to schedule a periodic task at a specific time, use the celery.schedules.crontab schedule behavior

'''

import time
import subprocess
import os
import shlex
import pickle
import cx_Oracle 
import socket
import sys
import platform

#from models import Suite, SuiteError, TestRun, TestError
#from django.db.models import Q
#from django.db.models import Max

#First argument: name of the current module 'tasks.py'
#Note: this is needed so that names can be automatically generated
#Second argument: specifies the URL of the message broker you want to use
#Note: we are using RabbitMQ
#celery = Celery('tasks', broker='amqp://guest@localhost//')

#Use the amqp result backend, which sends states as messages
#celery = Celery('tasks', backend='amqp', broker='amqp://')

#from celery.task import task
from celery import task
#from celery.task import Task, PeriodicTask
from celery import Task
from celery.task import PeriodicTask
from celery.registry import tasks

# ****************************** #
# Need to running scheduled tasks
#from celery.task.schedules import crontab
#from celery.decorators import periodic_task

from celery.schedules import crontab
from celery.task import periodic_task
# ****************************** #

from datetime import timedelta

#see https://bitbucket.org/fajran/irgsh-web/src/1dd46ae137ac/irgsh_web/build/tasks.py

#========================================================================#
class RetryTest(Task):
    abstract = True
    
    def on_success(self, retval, task_id, args, kwargs):
        logger.info("Task - RetryTest: %s - success" % task_id)
        
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.info("Task - RetryTest: %s - failure" % task_id)


@task(base=RetryTest, name="test_bench.tasks.RetryTest", max_retries=2)
def retry_test(env_var):
    logger.info("environment variable: " % env_var)
    logger.info("retry_test id:%s", retry_test.request.id)
    logger.info("retries:%s", retry_test.request.retries)

    foo = {'bar': 0}

    if retry_test.request.retries > 10:
        return True
    else:
        try:
            foo['foo']
        except KeyError as exc:
            retry_test.retry(exc=exc, countdown=5)

class PrintTask(Task):
    abstract = True
    
    def on_success(self, retval, task_id, args, kwargs):
        logger.info("Task - PrintTask: %s - success" % task_id)
        
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.info("Task - PrintTask: %s - failure" % task_id)

@task(base=PrintTask, name="test_bench.tasks.PrintTask")
def print_task():
    logger.info("print task was run...")
    

class MyTask(Task):
    abstract = True
    
    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        if self.max_retries == self.request_retries:
            self.state = states.FAILURE

@task(base=MyTask, name="test_bench.tasks.MyTask")
def err(x):
    try:
        if x < 3:
           raise Exception
        else:
            return x + 1
    except Exception as exp:
        logger.info("retrying")
        raise err.retry(args=[x], exc=exp, countdown=5, max_retries=3)
        

class MulTask(Task):
    abstract = True
    
    def on_success(self, retval, task_id, args, kwargs):
        logger.info("Task - MulTask - success")
        
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.info("Task - MulTask - failure")   
        
@task(base=MulTask, name="test_bench.tasks.MulTask")
def mul(x,y, *args, **kwargs):
    mult = x * y
    #return "The multiplication of " + str(x) + " and " + str(y) + " is: " + str(mult)
    return x * y


'''
#@task(name="test_bench.tasks.SumTask")
class SumTask(Task):
    #def __init__(self):
    #    self.x = 1
    #    self.y = 2
    def run(self, x,y):
        sum = x + y
        return "The sum is "+str(sum)

tasks.register(SumTask)
'''

class SumTask(Task):
    
    abstract = True

    def on_success(self, retval, task_id, args, kwargs):
        logger.info("Task - SumTask - success")
        
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.info("Task - SumTask - failure")   
        
    def after_return(self, *args, **kwargs):
        logger.info('Task returned: %r' % (self.request,)) #<Context: {u'chord': None, u'retries': 0, u'args': [2, 2], 'is_eager': False, u'errbacks': None, u'taskset': None, '_children': [], u'id': u'sum-task-a5b650fb-4884-4202-997b-c9caf37b14fb', 'called_directly': False, u'utc': True, u'task': u'test_bench.tasks.SumTask', 'group': None, u'callbacks': None, 'delivery_info': {'priority': None, 'routing_key': u'testbench.testagent20', 'exchange': u'testbench'}, 'hostname': 'nj1dvgtsxp20', u'expires': None, u'eta': None, u'kwargs': {}, '_protected': 1}>
    
@task(base=SumTask, name="test_bench.tasks.SumTask")
def add(x,y, *args, **kwargs):
    sum = x + y
    return "The sum is "+str(sum)


class SumAndMultiply(Task):

    abstract = True
    
    def on_success(self, retval, task_id, args, kwargs):
        logger.info("Task - SumAndMultiply - success")
        
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.info("Task - SumAndMultiply - failure")           
    
@task(base=SumAndMultiply, name="test_bench.tasks.SumAndMultiply")
def run_sum_and_multiply(*args, **kwargs):
    from celery import chain
    chain = SumTask().s(2,2) | MulTask().s(4,)
    chain()
    #res = chain(DeployPackage().s(), RunPackage().s())

#========================================================================#

class DeployPackage(Task):
    ''' 
    A task that deploys packaging
    '''
    
    abstract = True
                
    def on_success(self, retval, task_id, args, kwargs):
        logger = self.get_logger()
        logger.info("Task - DeployPackage - success")
        
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        ''' Handler called if the task raised an exception.'''
        #Note if the task raises an exception it is still acknowledged!
        #acks_late setting would be used when you need the task to be executed again
        #if the worker (for some reason) crashes mid-execution.
        logger = self.get_logger()
        logger.info("Task - DeployPackage - failure")    

#@task(base=DeployPackage, name="test_bench.tasks.DeployPackage")
@task(base=DeployPackage, name="tasks.DeployPackage")
def deploy_package(self, job, spec, suite, owner, **kwargs):
    logger = self.get_logger()
    logger.info("Start deploying package for spec: %s" % spec)
    
    #TODO: put build server and download file into config file
    from cStringIO import StringIO
    from zipfile import ZipFile, BadZipfile, LargeZipFile
    import requests
    results = requests.get('http://atsbuildserver:8111/guestAuth/repository/download/package_PackageBootstrap/latest.lastSuccessful/PackageBootstrap.zip')
    if results.ok:
        z = ZipFile(StringIO(results.content))
        try:
            if sys.platform == "win32": #platform.system() == "Windows"
                z.extractall('C:\\TestBench\\package')
            elif sys.platform == "linux": #platform.system() == "Linux2"
                x.extractall('~/testbench/package')
            else:
                logger.error("Platform '%s' is not supported" % sys.platform)
            return "Deploy Package succeeded"
        except (BadZipfile, LargeZipFile), e:
            print "Error: ", e
            return "Deploy Package failed"
                
class DeployTests(Task):
    
    abstract = True
    
    def on_success(self, retval, task_id, args, kwargs):
        logger = self.get_logger()
        logger.info("Tasks - Deploy Tests -  success")

    #def on_failure(self, retval, task_id, args, kwargs):
    def on_failure(self, exc, id, args, kwargs, einfo):
        '''Handler called if task raises an exception.'''
        logger = self.get_logger()
        logger.info("Tasks - Deploy Tests -  failed")

@task(base=DeployTests, name="test_bench.tasks.DeployTests")
def deploy_tests(self, job, spec, suite, owner, **kwargs):
    logger = self.get_logger()
    logger.info("Start deploying tests for spec: %s" % spec)
    
    #TODO: put build server and download file into config file
    from cStringIO import StringIO
    from zipfile import ZipFile, BadZipfile, LargeZipFile
    import requests
    results = requests.get('http://atsbuildserver:8111/viewLog.html?buildTypeId=%s_ATDevTests&buildId=lastSuccessful' % spec)
    if results.ok:
        z = ZipFile(StringIO(results.content))
        try: 
            z.extractall('C:\\TestBench\\deploy\\ATDevTests')
            return "Deploy Tests succeeded"
        except (BadZipfile, LargeZipFile), e:
            print "Error: ", e
            return "Deploy Tests failed"
        
class RunPackage(Task):
    
    abstract = True

    def on_success(self, retval, task_id, args, kwargs):
        logger = self.get_logger()
        logger.info("on success")

    #def on_failure(self, retval, task_id, args, kwargs):
    def on_failure(self, exc, id, args, kwargs, einfo):
        '''Handler called if task raises an exception.'''
        logger = self.get_logger()
        logger.info("on failure")

@task(base=RunPackage, name="test_bench.tasks.RunPackage")
def run_package(self, job, spec, suite, owner, **kwargs):
    
    logger = self.get_logger()
    logger.info("Start running packaging for spec: %s" % spec)
    
    program_name = 'C:\\Python26\\python'
    package_cmd = 'C:\\TestBench\\package\\package.py'
    filter_arg = '--filter=testlab'
    spec_arg = '--spec=%s' % spec
    outdir_arg = '--outdir=C:/TestBench/deploy'
    db_arg = '--db'
    p4_arg = '--nolocalp4'
    nosync_arg = '--nosync'
    nocheck_arg = '--nocheck'
    arguments = [package_cmd, filter_arg, spec_arg, outdir_arg, db_arg, p4_arg, nosync_arg, nocheck_arg]
    command = [program_name]
    command.extend(arguments)
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    
    print "Out: ", out
    print "Err: ", err
    
    retCode = p.returncode
    print "Return Code: ", retCode
    
    logger.info("End running packaging for spec: %s" % spec)
    if retCode != 0:
        #raise ValueError, 'Run Package failed, return code: %s' % retCode
        return 'Run Package failed, return code: %s' % retCode
    else:
        return 'Run Package succeeded, return code: %s' % retCode 
    

class DeployAndRunPackage(Task):
    
    abstract = True
    
    def on_success(self, retval, task_id, args, kwargs):
    #def on_success(self, exc, id, args, kwargs, info):
        logger = self.get_logger()
        logger.info("on success")
        
    #def on_failure(self, retval, task_id, args, kwargs):
    #def on_failure(self, exc, id, args, kwargs, einfo):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger = self.get_logger()
        logger.info("on failure")  

@task(base=DeployAndRunPackage, name="test_bench.tasks.DeployAndRunPackage")
def deploy_and_run_package(self, job, spec, suite, owner, **kwargs):
    from celery import chain
    # DeployPackage -> RunPackage
    #res = chain(DeployPackage().s() | RunPackage().s())
    dres = deploy_package(job, spec, suite, **kwargs)
    print "Deploy package result: ", dres
    rres = run_package(job, spec, suite, **kwargs)
    print "Run package result: ", rres
    #TODO: add return dres and rres?

class CreateDB(Task):
    #name = "package.create_db"
    #serializer = "json"
    '''
    A task that creates the database
    '''
    
    abstract = True
                
    def on_success(self, retval, task_id, args, kwargs):
    #def on_success(self, exc, id, args, kwargs, info):
        logger = self.get_logger()
        logger.info("on success")
        
    #def on_failure(self, retval, task_id, args, kwargs):
    #def on_failure(self, exc, id, args, kwargs, einfo):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger = self.get_logger()
        logger.info("on failure")    

@task(base=CreateDB, name="test_bench.tasks.CreateDB")
def create_db(self, job, spec, suite, owner, **kwargs):
    logger = self.get_logger()
    logger.info("Start creating db for spec: %s" % spec)
    time.sleep(5)
    retCode = subprocess.call(['python', 'C:\\Users\\mdaloia\\Documents\\Python\\automatic_oracle_data_pump_backup.py'])
    
    time.sleep(2)
    logger.info("End create db completed for spec: %s" % spec)
    if retCode != 0:
        raise ValueError, 'Package failed, return code: %s' % retCode


####from django.test import TestCase
'''
class CeleryTestCaseBase(TestCase):

    def setUp(self):
        super(CeleryTestCaseBase, self).setUp()
        self.applied_tasks = []

        self.task_apply_async_orig = Task.apply_async

        @classmethod
        def new_apply_async(task_class, args=None, kwargs=None, **options):
            self.handle_apply_async(task_class, args, kwargs, **options)

        # monkey patch the regular apply_sync with our method
        Task.apply_async = new_apply_async

    def tearDown(self):
        super(CeleryTestCaseBase, self).tearDown()

        # Reset the monkey patch to the original method
        Task.apply_async = self.task_apply_async_orig

    def handle_apply_async(self, task_class, args=None, kwargs=None, **options):
        self.applied_tasks.append((task_class, tuple(args), kwargs))

    def assert_task_sent(self, task_class, *args, **kwargs):
        was_sent = any(task_class == task[0] and args == task[1] and kwargs == task[2]
                       for task in self.applied_tasks)
        self.assertTrue(was_sent, 'Task not called w/class %s and args %s' % (task_class, args))

    def assert_task_not_sent(self, task_class):
        was_sent = any(task_class == task[0] for task in self.applied_tasks)
        self.assertFalse(was_sent, 'Task was not expected to be called, but was.  Applied tasks: %s' % self.applied_tasks)
'''
#class RunTestSuite(CeleryTestCaseBase):

class RunTestSuite(Task):    

    abstract = True
        
    def getNextTest(self):
        #Remove first test from list and use as current test to run
        return self.testSuite.pop(0)
    
    def on_success(self, retval, task_id, args, kwargs):
        logger = self.get_logger()
        logger.info("Task - RetryTest: %s - success" % task_id)
        
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger = self.get_logger()
        logger.info("Task - RetryTest: %s - failure" % task_id)    
    
    '''
    def after_return(self, *args, **kwargs):
        logger.info('Task returned: %r' % (self.request,)) 
    '''
    
@task(base=RunTestSuite, name="test_bench.tasks.RunTestSuite", max_retries=2)
def run_test_suite(self, job, spec, suite, owner, build_id, agents_task, **kwargs):
    
    logger = self.get_logger()
    logger.info("run_test_suite id:%s", run_test_suite.request.id)
    logger.info("retries:%s", run_test_suite.request.retries)

    
    print "RunTestSuite - job: ", job
    print "RunTestSuite - spec: ", spec
    print "RunTestSuite - suite: ", suite
    print "RunTestSuite - build_id: ", build_id
    print "RunTestSuite - agents_task", agents_task
    print "RunTestSuite - kwargs: ", kwargs
    
    #TODO: set this environment variable on all agents - LN_AT_DEV_TEST_DIR=C:\TestBench\deploy\ATDevTests
    #suite = 'dir:ats/lpc'        
    suitename = suite.split(':')[1].replace("/", "\\")        
    atDevTestDir = os.environ['LN_AT_DEV_TEST_DIR']
    suiteDir = atDevTestDir+"\\"+suitename
    
    logger.info("Suite name is: %s" % suitename)
    logger.info("LN_AT_DEV_TEST_DIR is: %s" % atDevTestDir)
    logger.info("suiteDir is: %s" % suiteDir)
    
    #initialize test suite
    testSuite = []
    
    for r,d,t in os.walk(suiteDir):
        for tests in t:
            if tests.startswith("test_") and tests.endswith(".py"):
                print "Test name: ", tests
                testSuite.append(tests)
        
    num_of_tests_in_suite = len(testSuite)
    
    logger.info("Starting test run for suite: %s which has %i tests" % (suite, num_of_tests_in_suite))
    time.sleep(5)
    
    #Get list of tests to put into suite file for the particular agent
    testlist = []
    hostname = socket.gethostname() #nj1dvgtsxp03  
    for agent in agents_task:
        if 'testagent'+str(hostname[-2:].strip("0")) in agent[0]:
            testlist = agent[1]
            
    logger.info("Test list is %s" % testlist)        
    textFileName = suitename.split("\\")
    filename = "_".join(textFileName)
    suiteFile = "%s_suite.txt" % filename   
    logger.info("suite file name is %s" % suiteFile) #lpc_suite.txt
    
    #clean up for next test suite run
    if os.path.exists(suiteFile):
        os.remove(suiteFile)
    for tests in testlist:
        file = open(suiteFile, "a")
        file.write(tests+"\n")
    file.close()
    
    suiteFileName = 'C://TestBench//'+suiteFile
    s = suiteFileName.encode(sys.getfilesystemencoding())
    
    '''
    retCode = subprocess.call(shlex.split("'C:\\Python26\\python' 'C:\\TestBench\\deploy\\PyTroller\\pytroller.py' -t tbsuite -p %i -s %s --kill_rogue_procs" % (build_id, s)))
    if retCode != 0:
        raise ValueError, 'Test Run failed, return code: %s' % retCode
    '''
    
    '''
    try:
        #pytroller = PyTroller()
        subprocess.call(shlex.split("'C:\\Python26\\python' 'C:\\TestBench\\deploy\\PyTroller\\pytroller.py' -t tbsuite -p %i -s %s --kill_rogue_procs" % (build_id, s)))
    #except pytroller.PyTroller, exc:
    except Exception, exc:
        #raise run_test_suite.retry(countdown=5, exc=exc)
        run_test_suite.retry(countdown=5, exc=exc)
    '''

    if run_test_suite.request.retries > 10:
        return True
    else:
        retCode = subprocess.call(shlex.split("'C:\\Python26\\python' 'C:\\TestBench\\deploy\\PyTroller\\pytroller.py' -t tbsuite -p %i -s %s --kill_rogue_procs" % (build_id, s)))
        if retCode != 0:
            run_test_suite.retry(countdown=5)
    
    #THIS WORKED
    '''
    for i in range(0, num_of_tests_in_suite):
        #Run single dvt
        testToRun = self.getNextTest()
        logger.info("Start running test: %s" % testToRun)
        retCode = subprocess.call(shlex.split("python 'C:\\TestBench\\deploy\\PyTroller\\pytroller.py' -p %s" % testToRun))
        if retCode != 0:
            raise ValueError, 'Test Run failed, return code: %s' % retCode           
    '''
        
    #Run test suite        
    #retCode = subprocess.call(shlex.split("python pytroller.py -p %s --sleep=1 -t suite")) % (os.environ['LN_AT_DEV_TEST_DIR']+'\\%s') % suitename
    #Run test directory
    #retCode = subprocess.call(shlex.split("python pytroller.py -t Dir -p %s")) % (os.environ['LN_AT_DEV_TEST_DIR']+'\\%s') % suitename
    time.sleep(2)
    logger.info("End test run for suite: %s" % suite)
        
    logger.info("Task - copy logs")
    copyres = CopyLogs().run(job, spec, suite, build_id, **kwargs)
        
    if failedExist:
        RunFailedTests(spec, suite)
                             

class RunFailedTests(Task):
    
    abstract = True
    
    def getNextTest(self):
        #Remove first test from list and use as current test to run
        return self.testSuite.pop(0)
    
    def on_success(self, retval, task_id, args, kwargs):
        logger = self.get_logger()
        logger.info("on success")
        
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger = self.get_logger()
        logger.info("on failure")    

@task(base=RunFailedTests, name="test_bench.tasks.RunFailedTests")
def run_failed_tests(self, spec, suite): # #trunk, dir:ats/indicationSuite

    #max_build_id = Suite.objects.latest('build_id')
    #build_id=max_build_id.build_id        
    #build_id = Suite.objects.all().aggregate(max_build_id=Max('build_id')) #build_id = {'max_build_id': 71816}
    #build_id = Suite.objects.filter(branch='trunk', suite_id='dir:ats/indicationSuite').aggregate(max_build_id=Max('build_id')) #build_id = {'max_build_id': 71816}
    #failed_tests_list = TestRun.objects.values('test_name').filter(build_id__in=max_build_id.build_id, run_successful='fail', known_issue='F')
    #for test in failed_tests_list: print test #{'test_name': u'test_mopo_unexecuted_midpeg'}
    
    build_id = Suite.objects.filter(branch=spec, suite_id=suite, tests_successful__gt=0).aggregate(max_build_id=Max('build_id'))
    max_id = build_id.get('max_build_id')
    failed_tests_list = TestRun.objects.values('test_name').filter(build_id=max_id, run_successful='fail', known_issue='F')
    num_failed_tests = len(failed_tests_list)
    
    for test in failed_tests_list: print test.get('test_name') #'test_mopo_unexecuted_midpeg'
    #build_id = Suite.objects.values('build_id').filter(branch=spec, suite_id=suite, build_type='P', tests_successful__gt=0).aggregate(max_end_time=Max('end_time'))
    #max_id = build_id.get('max_build_id')
    #TODO: combine 3 statements to get build_id in single query
    end_time = Suite.objects.filter(branch=spec, suite_id=suite, tests_successful__gt=0).aggregate(max_end_time=Max('end_time'))
    max_time = end_time.get('max_end_time') #datetime.datetime(2013, 7, 1, 20, 11, 57)
    build_id = Suite.objects.values('build_id').filter(end_time=max_time, branch=spec, suite_id=suite, build_type='P', tests_successful__gt=0)
    id = build_id[0].get('build_id')
    failed_tests_from_parent = TestRun.objects.values('test_name').filter(build_id=id, run_successful='fail', known_issue='F')
    
    for test in failed_tests_from_parent: print test.get('test_name') #test_mopo_unexecuted_midpeg
        

class CopyLogs(Task):

    '''
    A task that copies log files
    '''
    
    abstract = True
    
    def on_success(self, retval, task_id, args, kwargs):
        logger = self.get_logger()
        logger.info("logs were copied successfully")
        
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger = self.get_logger()
        logger.info("copy logs task failed")          

@task(base=CopyLogs, name="test_bench.tasks.CopyLogs")
def copy_logs(self, job, spec, suite, build_id, **kwargs):
    logger = self.get_logger()
    logger.info("Start copying logs for suite: %s" % suite)
    time.sleep(5)
    
    import os, shutil
    logDir = os.environ['LN_LOG_DIRECTORY']
    source = os.listdir(logDir)
    destination = "C:\\TestBench\\testlogs\\"+str(build_id)+"\\"
    if not os.path.exists(destination):
        os.mkdir(destination)
    for files in source:
        if files.endswith(".log"):
            shutil.move(logDir+"\\"+files,destination)


@task(ignore_result=True) #False
def lazy_job(name):
    logger = lazy_job.get_logger()
    logger.info('Starting the lazy job: {0}'.format(name))
    time.sleep(5)
    logger.info('Lazy job {0} completed'.format(name))

#@task(ignore_result=True)
@periodic_task(run_every=timedelta(minutes=5))
def p4_sync(name):
    pass

'''
@task(ignore_result=False)
def deploy_all(name):
    pass    

#NOTE: If the task is set to ignore_result (which it is by default in the latest version) it will stay at PENDING and not go to SUCCESS.
#http://docs.celeryproject.org/en/latest/userguide/tasks.html#states
#TODO: also define custom states: http://docs.celeryproject.org/en/latest/userguide/tasks.html#custom-states
@task(ignore_result=False)
def create_db(name):

    logger = create_db.get_logger()
    logger.info('Starting to create DB: {0}'.format(name))
    time.sleep(3)
    logger.info('Create DB {0} completed'.format(name))

@task(ignore_result=False)
def deploy_package(name):

    logger = deploy_package.get_logger()        
    logger.info('Starting to deploy package: {0}'.format(name))
    time.sleep(3)
    #subprocess.call(['python', 'C:\\depot\\mdaloia_NY0D7MDALOIA\\deploy\\package\\package.py'])
    subprocess.call(['python', 'C:\\tmp\\output_ln_home.py'])
    time.sleep(3)    
    logger.info('Deploy package {0} completed'.format(name))


#@task(ignore_result=False)
#Add my own remote control command
from celery.worker.control import Panel
@Panel.register
def deploy_tests(panel, **kwargs):
    panel.consumer.reset_connection()
    return {"ok": "connection re-established"}


@task(ignore_result=False)
def run_tests(name):
    pass    

@task(ignore_result=False)
def run_suite(name):
    pass    

@periodic_task(run_every=timedelta(minutes=1))
def run_failed_tests(*args, **kwargs):
    #job = group(run_tests(t) for t in tests)
    #job.apply_async()
    pass
'''

# this will run every minute, see http://celeryproject.org/docs/reference/celery.task.schedules.html#celery.task.schedules.crontab  
@periodic_task(run_every=crontab(hour="*", minute="*", day_of_week="*"))  
def test():      
    print "firing test task"                    

@periodic_task(run_every=crontab(hour=7, minute=30, day_of_week="sun"))  
def every_sunday_morning():      
    print("This is run every Sunday morning at 7:30")      
    
@periodic_task(run_every=crontab(hour=9, minute=54, day_of_week="tue"))  
def every_tuesday_morning():      
    print("This is run every Tuesday morning at 9:50")  

class SendEmail(Task):

    '''
    A task that copies log files
    '''
    
    abstract = True
    
    def on_success(self, retval, task_id, args, kwargs):
        logger = self.get_logger()
        logger.info("email sent success")
        
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger = self.get_logger()
        logger.info("email sent failure")          

@task(base=SendEmail, name="test_bench.tasks.SendEmail")    
def sendEmail(self, email):
    import win32com.client as W
    
    logger = self.get_logger()    
    logger.info("SendingEmail", "Started")
    #TODO: define emailheader, timestr, status
    message = emailheader + "Oracle Data Pump Backup: " + timestr + "\n"

    message += "\nCommand Status:\n"
    for s in status:
        if s != 'removeOldBackups':
            message += "\t" + s + ": "
            if status[s] == 0:
                message += "Success\n"
            elif status[s] == -1:
                message += "NOP\n"
            else:
                message += "Failed\n"
        
    message += "\nOld Backup Removal:\n"
    for f in status['removeOldBackups']:
        message += "\t" + f[1] + " removing backup file: " + f[0] + "\n"
            
            
    profilename='Outlook' 
    olook = W.gencache.EnsureDispatch("%s.Application" %profilename)
    mail = olook.CreateItem(W.constants.olMailItem)
    #TODO: pass in email recipient
    #mail.Recipients.Add(['mdaloia@liquidnet.com'])
    mail.Recipients.Add([email])
    #mail.Subject = 'Test'
    mail.Subject = emailheader
    #mail.Body = 'Test sending email via Python script'
    mail.Body = message
    mail.Send()
               
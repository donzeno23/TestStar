import time
import subprocess
import os
import shlex
import pickle
import cx_Oracle 
import socket
import sys
import platform

from celery import task
from celery import Task
from celery.task import PeriodicTask
from celery.registry import tasks

# ****************************** #
# Need for running scheduled tasks
from celery.schedules import crontab
from celery.task import periodic_task
# ****************************** #

from datetime import timedelta

import ConfigParser

from models import Suite, SuiteError, TestRun, TestError
from django.db.models import Q
from django.db.models import Max

#========================================================================#
class RetryTest(Task):
    abstract = True
    
    def on_success(self, retval, task_id, args, kwargs):
        logger.info("Task - RetryTest: %s - success" % task_id)
        
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.info("Task - RetryTest: %s - failure" % task_id)


@task(base=RetryTest, name="tasks.RetryTest", max_retries=2)
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

@task(base=PrintTask, name="tasks.PrintTask")
def print_task():
    logger.info("print task was run...")
    

class MyTask(Task):
    abstract = True
    
    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        if self.max_retries == self.request_retries:
            self.state = states.FAILURE

@task(base=MyTask, name="tasks.MyTask")
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
        
@task(base=MulTask, name="tasks.MulTask")
def mul(x,y, *args, **kwargs):
    mult = x * y
    #return "The multiplication of " + str(x) + " and " + str(y) + " is: " + str(mult)
    return x * y


class SumTask(Task):
    
    abstract = True

    def on_success(self, retval, task_id, args, kwargs):
        logger.info("Task - SumTask - success")
        
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.info("Task - SumTask - failure")   
        
    def after_return(self, *args, **kwargs):
        logger.info('Task returned: %r' % (self.request,))
    
@task(base=SumTask, name="tasks.SumTask")
def add(x,y, *args, **kwargs):
    sum = x + y
    return "The sum is "+str(sum)


class SumAndMultiply(Task):

    abstract = True
    
    def on_success(self, retval, task_id, args, kwargs):
        logger.info("Task - SumAndMultiply - success")
        
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.info("Task - SumAndMultiply - failure")           
    
@task(base=SumAndMultiply, name="tasks.SumAndMultiply")
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
        #NOTE: if the task raises an exception it is still acknowledged!
        #      acks_late setting would be used when you need the task to be executed again
        #      if the worker (for some reason) crashes mid-execution.
        logger = self.get_logger()
        logger.info("Task - DeployPackage - failure")    

@task(base=DeployPackage, name="tasks.DeployPackage")
def deploy_package(self, job, spec, suite, owner, **kwargs):
    logger = self.get_logger()
    logger.info("Start deploying package for spec: %s" % spec)
    
    #TODO: put build server and download file into config file
    from cStringIO import StringIO
    from zipfile import ZipFile, BadZipfile, LargeZipFile
    import requests
    Config = ConfigParser.ConfigParser()
    Config.read('tasks.ini')
    url = Config.get('buildserver', 'url')
    url_path = Config.get('buildserver', 'url_build_path')
    build_url = url+url_path
    build_filename = Config.get('buildserver', 'package_filename')    
    results = requests.get(build_url+build_filename)
    if results.ok:
        z = ZipFile(StringIO(results.content))
        try:
            if sys.platform == "win32": #platform.system() == "Windows"
                z.extractall('C:\\TestBench\\package')
            elif sys.platform == "linux": #platform.system() == "Linux2"
                z.extractall(os.environ['HOME']+'/testbench/package')
            else:
                logger.error("Platform '%s' is not supported" % sys.platform)
            return "Deploy Package succeeded"
        except (BadZipfile, LargeZipFile), e:
            #TODO: log error
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

@task(base=DeployTests, name="tasks.DeployTests")
def deploy_tests(self, job, spec, suite, owner, **kwargs):
    logger = self.get_logger()
    logger.info("Start deploying tests for spec: %s" % spec)
    
    #TODO: put build server and download file into config file
    from cStringIO import StringIO
    from zipfile import ZipFile, BadZipfile, LargeZipFile
    import requests
    Config = ConfigParser.ConfigParser()
    Config.read('tasks.ini')
    url = Config.get('buildserver', 'url')
    url_path = Config.get('buildserver', 'url_test_path')
    test_url = url+url_path
    results = requests.get(test_url % spec)
    if results.ok:
        z = ZipFile(StringIO(results.content))
        try: 
            if platform.system() == "Windows":
                z.extractall('C:\\TestBench\\deploy\\ATDevTests')
            elif platform.system() == "Linux":
                z.extractall(os.environ['HOME']+'/testbench/package')
            else:
                logger.error("Platform '%s' is not supported" % platform.system())
            return "Deploy Tests succeeded"
        except (BadZipfile, LargeZipFile), e:
            #TODO: log error
            print "Error: ", e
            return "Deploy Tests failed"
        
class RunPackage(Task):
    
    abstract = True

    def on_success(self, retval, task_id, args, kwargs):
        logger = self.get_logger()
        logger.info("on success")

    def on_failure(self, exc, id, args, kwargs, einfo):
        '''Handler called if task raises an exception.'''
        logger = self.get_logger()
        logger.info("on failure")

@task(base=RunPackage, name="tasks.RunPackage")
def run_package(self, job, spec, suite, owner, **kwargs):
    
    logger = self.get_logger()
    logger.info("Start running packaging for spec: %s" % spec)
    
    Config = ConfigParser.ConfigParser()
    Config.read('tasks.ini')   

    program_name = Config.get('package_info', 'program_name') 
    package_cmd = Config.get('package_info', 'package_cmd') 
    filter_arg = Config.get('package_info', 'filter_arg')
    spec_arg = Config.get('package_info', 'spec_arg') 
    outdir_arg = Config.get('package_info', 'outdir_arg')
    db_arg = Config.get('package_info', 'db_arg') 
    p4_arg = Config.get('package_info', 'p4_arg') 
    nosync_arg = Config.get('package_info', 'nosync_arg')
    nocheck_arg = Config.get('package_info', 'nocheck_arg')
    arguments = [package_cmd, filter_arg, spec_arg, outdir_arg, db_arg, p4_arg, nosync_arg, nocheck_arg]
    command = [program_name]
    command.extend(arguments)
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
        
    retCode = p.returncode
    
    logger.info("End running packaging for spec: %s" % spec)
    if retCode != 0:
        return 'Run Package failed, return code: %s' % retCode
    else:
        return 'Run Package succeeded, return code: %s' % retCode 
    

class DeployAndRunPackage(Task):
    
    abstract = True
    
    def on_success(self, retval, task_id, args, kwargs):
        logger = self.get_logger()
        logger.info("on success")
        
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger = self.get_logger()
        logger.info("on failure")  

@task(base=DeployAndRunPackage, name="tasks.DeployAndRunPackage")
def deploy_and_run_package(self, job, spec, suite, owner, **kwargs):
    from celery import chain
    #TODO: use celery chain methods
    # DeployPackage -> RunPackage
    #res = chain(DeployPackage().s() | RunPackage().s())
    #TODO: log results?
    dres = deploy_package(job, spec, suite, **kwargs)
    rres = run_package(job, spec, suite, **kwargs)
    #TODO: add return dres and rres?

class CreateDB(Task):
    #name = "package.create_db"
    #serializer = "json"
    '''
    A task that creates the database
    '''
    
    abstract = True
                
    def on_success(self, retval, task_id, args, kwargs):
        logger = self.get_logger()
        logger.info("on success")
        
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger = self.get_logger()
        logger.info("on failure")    

@task(base=CreateDB, name="tasks.CreateDB")
def create_db(self, job, spec, suite, owner, **kwargs):
    logger = self.get_logger()
    logger.info("Start creating db for spec: %s" % spec)
    time.sleep(5)
    retCode = subprocess.call(['python', 'automatic_oracle_data_pump_backup.py'])
    
    time.sleep(2)
    logger.info("End create db completed for spec: %s" % spec)
    if retCode != 0:
        raise ValueError, 'Package failed, return code: %s' % retCode


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
    
@task(base=RunTestSuite, name="tasks.RunTestSuite", max_retries=2)
def run_test_suite(self, job, spec, suite, owner, build_id, agents_task, **kwargs):
    
    logger = self.get_logger()
    logger.info("run_test_suite id:%s", run_test_suite.request.id)
    logger.info("retries:%s", run_test_suite.request.retries)

    
    logger.info("RunTestSuite - job:%s " %  job)
    logger.info("RunTestSuite - spec:%s " %  spec)
    logger.info("RunTestSuite - suite:%s " %  suite)
    logger.info("RunTestSuite - build_id:%s " %  build_id)
    logger.info("RunTestSuite - agents_task:%s " %  agents_task)
    logger.info("RunTestSuite - kwargs:%s " %  kwargs)

    atDevTestDir = os.environ['LN_AT_DEV_TEST_DIR']

    if platform.system() == "Windows":
        suitename = suite.replace("-", "\\") 
        suiteDir = atDevTestDir+"\\"+suitename
    elif platform.system() == "Linux":
        suitename = suite.replace("-", "/") 
        suiteDir = atDevTestDir+"/"+suitename
    else:
        logger.error("Unsupported platform '%s' is being used" % platform.system())
    

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
    hostname = socket.gethostname() 
    for agent in agents_task:
        if 'testagent'+str(hostname[-2:].strip("0")) in agent[0]:
            testlist = agent[1]
            
    logger.info("Test list is %s" % testlist) 
    if platform.system() == "Windows":
        textFileName = suitename.split("\\")
    elif platform.system() == "Linux":
        textFileName = suitename.split("/")
    else:
        logger.error("Unsupported platform '%s' is being used" % platform.system())
    filename = "_".join(textFileName)
    suiteFile = "%s_suite.txt" % filename   
    logger.info("suite file name is %s" % suiteFile)
    
    #clean up for next test suite run
    if os.path.exists(suiteFile):
        os.remove(suiteFile)
    for tests in testlist:
        file = open(suiteFile, "a")
        file.write(tests+"\n")
    file.close()
    
    if platform.system() == "Windows":
        suiteFileName = 'C://TestBench//'+suiteFile
    elif platform.system() == "Linux":
        suiteFileName = os.environ['HOME']+'/TestBench/'+suiteFile
    else:
        logger.error("Unsupported platform '%s' is being used" % platform.system())

    s = suiteFileName.encode(sys.getfilesystemencoding())
    
    if run_test_suite.request.retries > 10:
        return True
    else:
        Config = ConfigParser.ConfigParser()
        Config.read('tasks.ini')
        program_name = Config.get('package_info', 'program_name') 
        app_cmd = Config.get('package_info', 'app_cmd') 
        kill_procs_arg = Config.get('package_info', 'kill_procs_arg')
        retCode = subprocess.call(shlex.split("program_name app_cmd -t tbsuite -p %i -s %s kill_procs_arg" % (build_id, s)))
        if retCode != 0:
            run_test_suite.retry(countdown=5)
            
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

@task(base=RunFailedTests, name="tasks.RunFailedTests")
def run_failed_tests(self, spec, suite): 
    
    build_id = Suite.objects.filter(branch=spec, suite_id=suite, tests_successful__gt=0).aggregate(max_build_id=Max('build_id'))
    max_id = build_id.get('max_build_id')
    failed_tests_list = TestRun.objects.values('test_name').filter(build_id=max_id, run_successful='fail', known_issue='F')
    num_failed_tests = len(failed_tests_list)
    
    for test in failed_tests_list: print test.get('test_name') 
    #TODO: combine 3 statements to get build_id in single query
    end_time = Suite.objects.filter(branch=spec, suite_id=suite, tests_successful__gt=0).aggregate(max_end_time=Max('end_time'))
    max_time = end_time.get('max_end_time') #format: datetime.datetime(2013, 7, 1, 20, 11, 57)
    build_id = Suite.objects.values('build_id').filter(end_time=max_time, branch=spec, suite_id=suite, build_type='P', tests_successful__gt=0)
    id = build_id[0].get('build_id')
    failed_tests_from_parent = TestRun.objects.values('test_name').filter(build_id=id, run_successful='fail', known_issue='F')
    
    for test in failed_tests_from_parent: print test.get('test_name') 
        

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

@task(base=CopyLogs, name="tasks.CopyLogs")
def copy_logs(self, job, spec, suite, build_id, **kwargs):
    logger = self.get_logger()
    logger.info("Start copying logs for suite: %s" % suite)
    time.sleep(5)
    
    import os, shutil
    logDir = os.environ['LN_LOG_DIRECTORY']
    source = os.listdir(logDir)
    if platform.system() == "Windows":
        destination = "C:\\TestBench\\testlogs\\"+str(build_id)+"\\"
    elif platform.system() == "Linux":
        destination = os.environ['HOME']+'/TestBench/testlogs/'+str(build_id)+'/'
    else:
        logger.error("Unsupported platform '%s' is being used" % platform.system())
    if not os.path.exists(destination):
        os.mkdir(destination)
    for files in source:
        if files.endswith(".log"):
            if platform.system() == "Windows":
                shutil.move(logDir+"\\"+files,destination)
            elif platform.system() == "Linux":
                shutil.move(logDir+"/"+files,destination)
            else:
                logger.error("Unsupported platform '%s' is being used" % platform.system())


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

@task(base=SendEmail, name="tasks.SendEmail")    
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
    #mail.Recipients.Add(['jsmith@server.com'])
    mail.Recipients.Add([email])
    #mail.Subject = 'Test'
    mail.Subject = emailheader
    #mail.Body = 'Test sending email via Python script'
    mail.Body = message
    mail.Send()
               
(1)
api\control.py

class WorkerDeployPackage(ControlHandler):
    print "Calling WorkerDeployPackage..."
    
    @web.authenticated
    def post(self, taskid, workername):
        ...
        
        
    Traceback (most recent call last):
      File "C:\Python27\lib\site-packages\tornado\web.py", line 1141, in _when_complete
        callback()
      File "C:\Python27\lib\site-packages\tornado\web.py", line 1162, in _execute_method
        self._when_complete(method(*self.path_args, **self.path_kwargs),
      File "C:\Python27\lib\site-packages\tornado\web.py", line 2293, in wrapper
        return method(self, *args, **kwargs)
    TypeError: post() takes exactly 3 arguments (2 given)
    

(2)
models.py

C:\Users\mdaloia\TARTworkspace\TBWin\web\pyTB>python teststar --broker=amqp:// --broker_api=http://guest:guest@localhost:55672/api/
Initialize BaseHandler...
Traceback (most recent call last):
  File "C:\Python27\lib\runpy.py", line 162, in _run_module_as_main
    "__main__", fname, loader, pkg_name)
  File "C:\Python27\lib\runpy.py", line 72, in _run_code
    exec code in run_globals
  File "C:\Users\mdaloia\TARTworkspace\TBWin\web\pyTB\teststar\__main__.py", line 4, in <module>
    from command import TestStarCommand
  File "teststar\command.py", line 13, in <module>
    from app import TestStar
  File "teststar\app.py", line 32, in <module>
    from urls import handlers
  File "teststar\urls.py", line 5, in <module>
    from views.workers import (
  File "teststar\views\workers.py", line 6, in <module>
    from models import WorkersModel, WorkerModel
  File "teststar\models.py", line 151, in <module>
    class Suite(models.Model):
  File "C:\Python27\lib\site-packages\django\db\models\base.py", line 93, in __new__
    kwargs = {"app_label": model_module.__name__.split('.')[-2]}
IndexError: list index out of range

class TestError(models.Model):
    #id = models.DecimalField(unique=True, max_digits=0, decimal_places=-127)
    id = models.DecimalField(unique=True, primary_key=True, max_digits=11, decimal_places=0)
    test = models.ForeignKey(TestRun)
    #error_group = models.CharField(max_length=4000, blank=True) #DatabaseError: ORA-00910: specified length too long for its datatype
    error_group = models.CharField(max_length=2000, blank=True)
    error_message = models.TextField(blank=True)
    exception_trace = models.TextField(blank=True)
    exception_message = models.TextField(blank=True)
    target_area_reason = models.CharField(max_length=500, blank=True)
    known_issue_reason = models.CharField(max_length=500, blank=True)
    execution_summary = models.TextField(blank=True)
    class Meta:
        app_label='dj'
        db_table = u'test_error'
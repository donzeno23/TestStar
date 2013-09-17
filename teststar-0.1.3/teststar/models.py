from __future__ import absolute_import
from __future__ import with_statement

from celery.utils.compat import OrderedDict

from django.db import models
import datetime

class BaseModel(object):
    def __init__(self, app):
        self.app = app

    def __eq__(self, other):
        raise NotImplementedError

    def __ne__(self, other):
        return not self.__eq__(other)


class WorkersModel(BaseModel):
    def __init__(self, app):
        super(WorkersModel, self).__init__(app)
        self.workers = OrderedDict()

        state = self.app.state
        for workername, stat in sorted(state.stats.iteritems()):
            pool = stat.get('pool') or {}
            self.workers[workername] = dict(
                status=(workername in state.ping),
                concurrency=pool.get('max-concurrency'),
                completed_tasks=sum(stat['total'].itervalues()),
                running_tasks=len(state.active_tasks.get(workername, [])),
                reserved_tasks=len(state.reserved_tasks.get(workername, [])),
                queues=map(lambda x: x['name'],
                           state.active_queues.get(
                           workername, [])),
            )

    @classmethod
    def get_latest(cls, app):
        return WorkersModel(app)

    @classmethod
    def get_workers(cls, app):
        return app.state.stats.keys()

    @classmethod
    def is_worker(cls, app, workername):
        return WorkerModel.get_worker(app, workername) is not None

    def __eq__(self, other):
        return other is not None and self.workers == other.workers


class WorkerModel(BaseModel):
    def __init__(self, app, name):
        super(WorkerModel, self).__init__(app)

        state = self.app.state
        self.name = name
        self.stats = state.stats[name]
        self.active_tasks = state.active_tasks.get(name, {})
        self.scheduled_tasks = state.scheduled_tasks.get(name, {})
        self.active_queues = state.active_queues.get(name, {})
        self.revoked_tasks = state.revoked_tasks.get(name, [])
        self.registered_tasks = filter(lambda x: not x.startswith('celery.'),
                                       state.registered_tasks.get(name, {}))
        self.reserved_tasks = state.reserved_tasks.get(name, {})
        self.conf = state.conf.get(name, {})

    @classmethod
    def get_worker(self, app, name):
        if name not in app.state.stats:
            return None
        return WorkerModel(app, name)

    def __eq__(self, other):
        return self.name == other.name and self.stats == other.stats and\
            self.active_tasks == other.active_tasks and\
            self.active_queues == other.active_queues and\
            self.revoked_tasks == other.revoked_tasks and\
            self.registered_tasks == other.registered_tasks and\
            self.scheduled_tasks == other.scheduled_tasks and\
            self.reserved_tasks == other.reserved_tasks and\
            self.conf == other.conf


class TaskModel(BaseModel):
    def __init__(self, app, task_id):
        super(TaskModel, self).__init__(app)

        task = app.events.state.tasks[task_id]

        self._fields = task._defaults.keys()
        for name in self._fields:
            if hasattr(task, name):
                setattr(self, name, getattr(task, name))

    @classmethod
    def get_task_by_id(cls, app, task_id):
        try:
            return TaskModel(app, task_id)
        except KeyError:
            return None

    @classmethod
    def iter_tasks(cls, app, limit=None, type=None, worker=None, state=None):
        i = 0
        events_state = app.events.state
        for uuid, task in events_state.tasks_by_timestamp():
            if type and task.name != type:
                continue
            if worker and task.worker.hostname != worker:
                continue
            if state and task.state != state:
                continue
            yield uuid, task
            i += 1
            if i == limit:
                break

    @classmethod
    def seen_task_types(cls, app):
        return app.events.state.task_types()

    def __dir__(self):
        return self._fields


class BrokerModel(BaseModel):
    def __init__(self, app):
        super(BrokerModel, self).__init__(app)

    @property
    def url(self):
        return self.app.celery_app.connection().as_uri()

    @property
    def queues(self):
        return self.app.state.broker_queues

    @property
    def info_available(self):
        if self.app.celery_app.connection().transport == 'amqp' and\
                not self.app.options.broker_api:
            return False
        return True

# Test Repository tables
#Moved higher up in file since there are foreign key dependencies and this needs to be defined first
class Suite(models.Model):
    #build_id = models.DecimalField(unique=True, max_digits=0, decimal_places=-127)
    #build_id = models.DecimalField(unique=True, max_digits=5, decimal_places=0, primary_key=True)
    build_id = models.IntegerField(unique=True, primary_key=True)
    suite_id = models.CharField(max_length=250)
    #start_time = models.DateField(null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    #end_time = models.DateField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.CharField(max_length=100, blank=True)
    machine_name = models.CharField(max_length=20, blank=True)
    anthill_project = models.CharField(max_length=250, blank=True)
    build_type = models.CharField(max_length=3, blank=True)
    anthill_build_number = models.CharField(max_length=50, blank=True)
    is_hypertest = models.CharField(max_length=3, blank=True)
    branch = models.CharField(max_length=50, blank=True)
    #suite_failures = models.DecimalField(null=True, max_digits=0, decimal_places=-127, blank=True)
    suite_failures = models.DecimalField(null=True, max_digits=5, decimal_places=0, blank=True)
    #tests_successful = models.DecimalField(null=True, max_digits=0, decimal_places=-127, blank=True)
    tests_successful = models.DecimalField(null=True, max_digits=5, decimal_places=0, blank=True)
    #tests_failures = models.DecimalField(null=True, max_digits=0, decimal_places=-127, blank=True)
    tests_failures = models.DecimalField(null=True, max_digits=5, decimal_places=0, blank=True)
    #project_id = models.DecimalField(null=True, max_digits=0, decimal_places=-127, blank=True)
    project_id = models.DecimalField(null=True, max_digits=5, decimal_places=0, blank=True)
    #suite_compiled = models.DecimalField(null=True, max_digits=0, decimal_places=-127, blank=True)
    suite_compiled = models.DecimalField(null=True, max_digits=5, decimal_places=0, blank=True)
    unit_model = models.CharField(max_length=1, blank=True)
    extra_info = models.CharField(max_length=250, blank=True)
    create_time = models.DateField(null=True, blank=True)
    class Meta:
        app_label='suite'
        db_table = u'suite'
    
    def __unicode__(self):
        return u'%s %s' % (self.build_id, self.suite_id)
    
    def was_created_today(self):
        return self.create_time == datetime.date.today()
    was_created_today.short_description = 'Created today?'

#Moved higher up in file since there are foreign key dependencies and this needs to be defined first
class TestRun(models.Model):
    #id = models.DecimalField(unique=True, max_digits=0, decimal_places=-127)
    id = models.DecimalField(unique=True, primary_key=True, max_digits=11, decimal_places=0)
    build = models.ForeignKey(Suite)
    test_name = models.CharField(max_length=250)
    run_successful = models.CharField(max_length=10)
    extra_info = models.CharField(max_length=250, blank=True)
    #start_time = models.DateField()
    start_time = models.DateTimeField()
    end_time = models.DateField(null=True, blank=True)
    package_id = models.CharField(max_length=250, blank=True)
    duration = models.CharField(max_length=100, blank=True)
    machine_name = models.CharField(max_length=100, blank=True)
    known_issue = models.CharField(max_length=3, blank=True)
    #checksum = models.DecimalField(null=True, max_digits=0, decimal_places=-127, blank=True)
    checksum = models.DecimalField(null=True, max_digits=11, decimal_places=0, blank=True)
    #revision = models.DecimalField(null=True, max_digits=0, decimal_places=-127, blank=True)
    revision = models.DecimalField(null=True, max_digits=5, decimal_places=0, blank=True)
    #duration_ms = models.DecimalField(null=True, max_digits=0, decimal_places=-127, blank=True)
    duration_ms = models.DecimalField(null=True, max_digits=11, decimal_places=0, blank=True)
    changelist_author = models.CharField(max_length=20, blank=True)
    #changelist_id = models.DecimalField(null=True, max_digits=0, decimal_places=-127, blank=True)
    changelist_id = models.DecimalField(null=True, max_digits=11, decimal_places=0, blank=True)
    failed_in_target_area = models.CharField(max_length=10, blank=True)
    contained_target_area = models.CharField(max_length=10, blank=True)
    class Meta:
        app_label='testrun'
        db_table = u'test_run'

    def __unicode__(self):
        return u'%s %s' % (self.id, self.build)


class SuiteError(models.Model):
    #id = models.DecimalField(unique=True, max_digits=0, decimal_places=-127)
    id = models.DecimalField(unique=True, primary_key=True, max_digits=11, decimal_places=0)
    build = models.ForeignKey(Suite)
    error_group = models.CharField(max_length=2000, blank=True)
    error_message = models.TextField(blank=True)
    exception_trace = models.TextField(blank=True)
    exception_message = models.TextField(blank=True)
    machine_name = models.CharField(max_length=20, blank=True)
    class Meta:
        app_label='suiteerror'
        db_table = u'suite_error'       

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
        app_label='testerror'
        db_table = u'test_error'

    def __unicode__(self):
        return u'%s %s' % (self.id, self.test)

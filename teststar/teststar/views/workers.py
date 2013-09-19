from __future__ import absolute_import

from tornado import web

import logging

from ..views import BaseHandler
from ..models import WorkersModel, WorkerModel

import os, platform
import ConfigParser

Config = ConfigParser.ConfigParser()

class WorkersView(BaseHandler):
    @web.authenticated
    def get(self):
        app = self.application
        workers = WorkersModel.get_latest(app).workers
        broker = app.celery_app.connection().as_uri()

        spec = self.get_argument('spec', None)
        suite = self.get_argument('suite', None)
        owner = self.get_argument('owner', None)

        if platform.system() == 'Windows':
            Config.read(os.environ['TESTSTAR_HOME']+'\\teststar.ini')
        elif platform.system() == "Linux":
            Config.read(os.environ['TESTSTAR_HOME']+'/teststar.ini')
        else:
            logging.error("Unsupported platform '%s' is being used" % platform.system())
        
        specs = {k:v for k,v in Config.items('spec')} 
        suites = [unicode(i[1]) for i in Config.items('suite')]
        owners = [unicode(i[1]) for i in Config.items('owner')]

        self.render("workers.html", workers=workers, broker=broker, specs=specs, suites=suites, owners=owners, spec=spec, suite=suite, owner=owner)


class WorkerView(BaseHandler):
    @web.authenticated
    def get(self, workername):
        app = self.application
        worker = WorkerModel.get_worker(app, workername)
        if worker is None:
            raise web.HTTPError(404, "Unknown worker '%s'" % workername)

        self.render("worker.html", worker=worker)

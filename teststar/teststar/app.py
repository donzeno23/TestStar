from tornado.options import options, define, parse_command_line
import django.core.handlers.wsgi
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi
#import daemon
import os, sys

import tornado.web
from tornado import ioloop

# django settings must be called before importing models
from django.conf import settings
settings.configure(DATABASE_ENGINE="django.db.backends.oracle", 
                   DATABASE_NAME="DEVDB7",
                   DATABASE_USER="test_repository",
                   DATABASE_PASSWORD="tr4qa",
                   DATABASE_HOST="devdb7.liquidnet.com",
                   DATABASE_PORT="1521")

from django import forms
from django.db import models


import celery

from teststar.events import Events
from teststar.state import State
from teststar.urls import handlers
#NOTE: the below is used when running python teststar ...
#from events import Events
#from state import State
#from urls import handlers


class TestStar(tornado.web.Application):
    def __init__(self, celery_app=None, events=None, state=None,
                 io_loop=None, options=None, **kwargs):
        kwargs.update(handlers=handlers)
        super(TestStar, self).__init__(**kwargs)
        self.io_loop = io_loop or ioloop.IOLoop.instance()
        self.options = options or object()
        self.auth = getattr(self.options, 'auth', [])
        self.basic_auth = getattr(self.options, 'basic_auth', None)
        self.broker_api = getattr(self.options, 'broker_api', None)
        self.ssl = None
        if options and self.options.certfile and self.options.keyfile:
            cwd = os.environ.get('PWD') or os.getcwd()
            self.ssl = {
                'certfile': os.path.join(cwd, self.options.certfile),
                'keyfile': os.path.join(cwd, self.options.keyfile),
            }

        self.celery_app = celery_app or celery.Celery()
        self.events = events or Events(celery_app, db=options.db,
                                       persistent=options.persistent,
                                       io_loop=self.io_loop,
                                       max_tasks_in_memory=options.max_tasks)
        self.state = State(celery_app, self.broker_api)

    def start(self):
        self.events.start()
        if self.options.inspect:
            self.state.start()
        self.listen(self.options.port, address=self.options.address,
                    ssl_options=self.ssl, xheaders=self.options.xheaders)
        self.io_loop.start()

    def stop(self):
        self.events.stop()

    
from tornado.options import options, define, parse_command_line
import django.core.handlers.wsgi
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi
import os, sys

import ConfigParser

import tornado.web
from tornado import ioloop

# django settings must be called before importing models
from django.conf import settings

#Get DB settings
Config = ConfigParser.ConfigParser()

if platform.system() == 'Windows':
    Config.read(os.environ['TESTSTAR_HOME']+'\\teststar.ini')
elif platform.system() == "Linux":
    Config.read(os.environ['TESTSTAR_HOME']+'/teststar.ini')
else:
    logging.info("Platform '%'s is not supported" % platform.system())

dbengine = Config.get('database', 'engine')    
dbname = Config.get('database', 'name')
dbuser = Config.get('database', 'user')
dbpassword = Config.get('database', 'password')
dbhost = Config.get('database', 'host')
dbport = Config.get('database', 'port')

settings.configure(DATABASES = {
    'default': {
        'ENGINE': dbengine,
        'NAME': dbname,
        'USER': dbuser,             # Not used with sqlite3.
        'PASSWORD': dbpassword,     # Not used with sqlite3.
        'HOST': dbhost,             # Set to empty string for localhost. Not used with sqlite3.
        'PORT': dbport,             # Set to empty string for default. Not used with sqlite3.            
    }
}
)

from django import forms
from django.db import models

import celery

from teststar.events import Events
from teststar.state import State
from teststar.urls import handlers


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

    
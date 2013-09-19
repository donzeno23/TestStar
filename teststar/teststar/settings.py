from __future__ import absolute_import

from os.path import join, abspath, dirname

from .utils import gen_cookie_secret


PROJECT_ROOT = abspath(dirname(__file__))

APP_SETTINGS = dict(
    template_path=join(PROJECT_ROOT, "templates"),
    static_path=join(PROJECT_ROOT, "static"),
    cookie_secret=gen_cookie_secret(),
    login_url='/login',
)

URL_PREFIX = ''
PAGE_UPDATE_INTERVAL = 2000
CELERY_EVENTS_ENABLE_INTERVAL = 5000
CELERY_INSPECT_TIMEOUT = 1000


BROKER_URL = 'amqp://guest:guest@localhost:5672//'

# Using rabbmitmq to store task state and results.
# Send results back as AMQP messages.
CELERY_RESULT_BACKEND = "amqp"
# Task messages will be acknowledged AFTER the task has been
# executed, not just before, which is the default behavior
CELERY_ACKS_LATE = True

#If enabled the worker pool can be restarted using the pool_restart remote control command.
CELERYD_POOL_RESTARTS = True
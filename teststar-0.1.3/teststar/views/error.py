from __future__ import absolute_import

import tornado.web

from ..views import BaseHandler
#NOTE: the below is used when running python teststar ...
#from views import BaseHandler


class NotFoundErrorHandler(BaseHandler):
    def get(self):
        raise tornado.web.HTTPError(404)

    def post(self):
        raise tornado.web.HTTPError(404)

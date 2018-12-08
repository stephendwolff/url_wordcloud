# -*- coding: utf-8 -*-
import os

import tornado.web
from tornado_sqlalchemy import make_session_factory

from .urls import url_patterns


class URLWordCloudApplication(tornado.web.Application):

    def __init__(self):
        factory = make_session_factory('mysql+mysqldb://urlwordcloud:urlwordcloud@localhost/urlwordcloud')

        # need pool_recycle option if connecting for longer than 8 hours
        # so would need to update tornado_sqlalchemy (ie fork and contribute)
        # pool_recycle=3600

        settings = dict(
            debug=True,             # NOT FOR PRODUCTION
            cookie_secret="gB9jYwVv0aodH51judoGwroWP",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=False,#xsrf_cookies,
            session_factory=factory,
            autoreload=True         # NOT FOR PRODUCTION ?
        )
        super(URLWordCloudApplication, self).__init__(url_patterns, **settings)

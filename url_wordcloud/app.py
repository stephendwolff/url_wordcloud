# -*- coding: utf-8 -*-
import logging
import os

import tornado.web
from tornado_sqlalchemy import make_session_factory

from .urls import url_patterns


class URLWordCloudApplication(tornado.web.Application):
    """
    Application for webpage word cloud analysis
    """
    def __init__(self, mysqluser, mysqlpassword, mysqlhost, mysqldatabase):

        mysql_connection_str = 'mysql+mysqldb://{0}:{1}@{2}/{3}'.format(
            mysqluser, mysqlpassword, mysqlhost, mysqldatabase
        )
        logging.info(mysql_connection_str)

        factory = make_session_factory(mysql_connection_str)

        # need pool_recycle option if connecting for longer than 8 hours
        # so would need to update tornado_sqlalchemy (ie fork and contribute)
        # pool_recycle=3600

        # NOT FOR PRODUCTION
        settings = dict(
            debug=True,
            cookie_secret="gB9jYwVv0aodH51judoGwroWP",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=False,
            session_factory=factory,
            autoreload=True
        )
        super(URLWordCloudApplication, self).__init__(url_patterns, **settings)

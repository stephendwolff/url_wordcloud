import os

import tornado.web

from .urls import url_patterns


class URLWordCloudApplication(tornado.web.Application):

    def __init__(self): #, database_name='', xsrf_cookies=True):
        settings = dict(
            debug=True,             # NOT FOR PRODUCTION
            cookie_secret="gB9jYwVv0aodH51judoGwroWP",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=False,#xsrf_cookies,
            autoreload=True         # NOT FOR PRODUCTION ?
        )
        super(URLWordCloudApplication, self).__init__(url_patterns, **settings)

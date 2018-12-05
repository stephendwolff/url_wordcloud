#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Basic run script"""

import logging
import os

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.autoreload
from tornado.options import define, options
import tornado.web

from url_wordcloud.urls import url_patterns

define("port", default=8888, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        settings = dict(
            cookie_secret="gB9jYwVv0aodH51judoGwroWP",
            template_path=os.path.join(os.path.dirname(__file__), "url_wordcloud", "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "url_wordcloud", "static"),
            xsrf_cookies=True,
        )
        super(Application, self).__init__(url_patterns, **settings)


def main():
    tornado.options.parse_command_line()
    app = Application()
    logging.info("Starting Application on port {0}".format(options.port))
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()

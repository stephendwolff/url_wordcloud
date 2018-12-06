#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

import tornado.autoreload
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

from url_wordcloud.app import URLWordCloudApplication

define("port", default=8888, help="run on the given port", type=int)



def main():
    tornado.options.parse_command_line()
    app = URLWordCloudApplication()
    logging.info("Starting Application on port {0}".format(options.port))
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()

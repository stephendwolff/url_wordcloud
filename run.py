#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import signal
import time

import tornado.autoreload
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.httpserver import HTTPServer
from tornado.options import define, options

from url_wordcloud.app import URLWordCloudApplication

from nacl.public import PrivateKey

from url_wordcloud.utils import generate_keys

MAX_WAIT_SECONDS_BEFORE_SHUTDOWN = 3

define("port", default=8888, help="run on the given port", type=int)
define("mysqluser", default='urlwordcloud', help="mysql username", type=str)
define("mysqlpassword", default='urlwordcloud', help="mysql password", type=str)
define("mysqlhost", default='localhost', help="mysql server hostname", type=str)
define("mysqldatabase", default='urlwordcloud', help="mysql database", type=str)


def sig_handler(sig, frame):
    logging.warning('Caught signal: %s', sig)
    tornado.ioloop.IOLoop.instance().add_callback(shutdown)


def shutdown():
    logging.info('Stopping http server')
    server.stop()

    logging.info('Will shutdown in %s seconds ...', MAX_WAIT_SECONDS_BEFORE_SHUTDOWN)
    io_loop = tornado.ioloop.IOLoop.instance()

    deadline = time.time() + MAX_WAIT_SECONDS_BEFORE_SHUTDOWN

    def stop_loop():
        now = time.time()

        # graceful shutdown code from https://gist.github.com/mywaiting/4643396
        # this must be pre Tornado 5, as the _callbacks attribute
        if now < deadline: # and (io_loop._callbacks or io_loop._timeouts):
            io_loop.add_timeout(now + 1, stop_loop)
        else:
            io_loop.stop()
        logging.info('Shutdown')

    stop_loop()


def main():
    tornado.options.parse_command_line()

    generate_keys()

    # use tornado HTTPServer, and add signal handling for graceful shutdown
    global server
    app = URLWordCloudApplication(options.mysqluser, options.mysqlpassword, options.mysqlhost, options.mysqldatabase)
    server = HTTPServer(app)
    server.listen(options.port)

    logging.info("Starting Application on port {0}".format(options.port))

    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)

    tornado.ioloop.IOLoop.current().start()

    logging.info("Exit...")


if __name__ == "__main__":
    main()

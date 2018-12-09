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


MAX_WAIT_SECONDS_BEFORE_SHUTDOWN = 3

define("port", default=8888, help="run on the given port", type=int)


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

    # Generate applications public and private key
    # In practice, these would be set externally and stored outside the repository
    sk = PrivateKey.generate()
    pk = sk.public_key

    # write to filesfor access if they don't exist
    sk_path = os.path.join(os.path.dirname(__file__), "private_key")
    if not os.path.exists(sk_path):
        # write as binary
        with open(sk_path, 'wb') as f:
            sk_bytes = bytes(sk)
            f.write(sk_bytes)

    pk_path = os.path.join(os.path.dirname(__file__), "public_key")
    if not os.path.exists(pk_path):
        with open(pk_path, 'wb') as f:
            pk_bytes = bytes(pk)
            f.write(pk_bytes)

    global server
    app = URLWordCloudApplication()
    server = HTTPServer(app)
    server.listen(options.port)

    logging.info("Starting Application on port {0}".format(options.port))

    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)

    tornado.ioloop.IOLoop.current().start()

    logging.info("Exit...")

if __name__ == "__main__":
    main()

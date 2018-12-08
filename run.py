#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os

import tornado.autoreload
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

from url_wordcloud.app import URLWordCloudApplication

from nacl.public import PrivateKey

define("port", default=8888, help="run on the given port", type=int)



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


    app = URLWordCloudApplication()

    logging.info("Starting Application on port {0}".format(options.port))
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()

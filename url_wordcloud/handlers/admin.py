# -*- coding: utf-8 -*-

import tornado.web


class AdminHandler(tornado.web.RequestHandler):

    @tornado.web.authenticated
    def get(self):
        self.render('admin.html')

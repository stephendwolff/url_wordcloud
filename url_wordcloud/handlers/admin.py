# -*- coding: utf-8 -*-
import tornado.escape
import tornado.web


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")


class AdminHandler(BaseHandler):
    def get(self):
        if not self.current_user:
            # TODO does Tornado have named URLs?
            self.redirect("/login/")
            return
        name = tornado.escape.xhtml_escape(self.current_user)

        # TODO how is context passed to templates?
        self.render('admin.html')


class LoginHandler(BaseHandler):
    def get(self):
        self.render('login.html')

    def post(self):
        self.set_secure_cookie("user", self.get_argument("name"))
        self.redirect("/admin/")


class LogoutHandler(BaseHandler):
    def get(self):
        self.set_secure_cookie("user", "")
        self.redirect('/login/')

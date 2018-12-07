# -*- coding: utf-8 -*-
import tornado.escape
import tornado.web
from tornado_sqlalchemy import SessionMixin

from url_wordcloud.models import Word


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")


class AdminHandler(SessionMixin, BaseHandler):
    def get(self):
        if not self.current_user:
            # TODO does Tornado have named URLs?
            self.redirect("/login/")
            return

        name = tornado.escape.xhtml_escape(self.current_user)

        with self.make_session() as session:
            words = session.query(Word).all()
            self.render("admin.html", words=words, name=name)



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

# -*- coding: utf-8 -*-
import os

import tornado.escape
import tornado.web
from tornado_sqlalchemy import SessionMixin

from url_wordcloud.models import Word
from url_wordcloud.utils import asymmetrically_decrypt


class BaseHandler(tornado.web.RequestHandler):
    """
    Base handler for any pages which need simple cookie based authentication
    """
    def get_current_user(self):
        return self.get_secure_cookie("user")


class AdminHandler(SessionMixin, BaseHandler):
    """
    Handler for '/admin/'
     - redirect it no current user found
     - return list of words ordered in reverse frequency order
     - decrypt on the fly
    """

    sk = None

    def __init__(self, application, request, **kwargs):
        sk_path = os.path.join(os.path.dirname(__file__), "..", "..", "private_key")

        with open(sk_path, 'rb') as f:
            self.sk = f.read()

        super(AdminHandler, self).__init__(application, request, **kwargs)

    def get(self):
        if not self.current_user:
            # TODO Investigate whether Tornado have named URLs?
            self.redirect("/login/")
            return

        name = tornado.escape.xhtml_escape(self.current_user)

        with self.make_session() as session:

            encrypted_words = session.query(Word).order_by(Word.frequency.desc()).all()
            words = []

            word: Word
            for word in encrypted_words:
                words.append({"word": asymmetrically_decrypt(word.word, self.sk), "frequency": word.frequency})

            self.render("admin.html", words=words, name=name)


class LoginHandler(BaseHandler):
    """
    Handler for '/login/'
    Very basic view for entering a username
    TODO, expand into fuller authentication, ie with password compared to db salted hashed user password
    """
    def get(self):
        self.render('login.html')

    def post(self):
        self.set_secure_cookie("user", self.get_argument("name"))
        self.redirect("/admin/")


class LogoutHandler(BaseHandler):
    """
    Handler for '/logout/'
    """
    def get(self):
        self.set_secure_cookie("user", "")
        self.redirect('/login/')

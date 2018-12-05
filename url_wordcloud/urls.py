# -*- coding: utf-8 -*-

from .handlers import base, admin


url_patterns = [
    (r"/", base.MainHandler),
    (r"/admin/", admin.AdminHandler),
    (r"/login/", admin.LoginHandler),
    (r"/logout/", admin.LogoutHandler),
    (r"/analyse_url/", base.AnalyseURLHandler),
]
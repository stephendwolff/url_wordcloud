# -*- coding: utf-8 -*-

from .handlers import base, admin


url_patterns = [
    # http handlers
    (r"/", base.MainHandler),
    (r"/admin/", admin.AdminHandler),
    (r"/login/", admin.LoginHandler),
    (r"/logout/", admin.LogoutHandler),

    # websocket handler
    (r"/analyse_url/", base.AnalyseURLHandler),
]
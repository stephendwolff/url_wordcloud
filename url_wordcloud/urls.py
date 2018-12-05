# -*- coding: utf-8 -*-

from .handlers import base, admin


url_patterns = [
    (r"/", base.MainHandler),
    (r"/admin/", admin.AdminHandler),
]
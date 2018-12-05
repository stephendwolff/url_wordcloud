# -*- coding: utf-8 -*-
import logging
import tornado.escape
import tornado.web
import tornado.websocket


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('index.html')


class AnalyseURLHandler(tornado.websocket.WebSocketHandler):
    def on_message(self, message):
        logging.info("got message %r", message)
        parsed = tornado.escape.json_decode(message)

        word_url = parsed["url_for_wordcloud"]




        # chat = {"id": str(uuid.uuid4()), "body": parsed["body"]}
        # chat["html"] = tornado.escape.to_basestring(
        #     self.render_string("message.html", message=chat)
        # )
        #
        # ResonatrHandler.update_cache(chat)
        # ResonatrHandler.send_updates(chat)
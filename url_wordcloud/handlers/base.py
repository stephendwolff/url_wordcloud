# -*- coding: utf-8 -*-
import logging
import re
from collections import Counter
from json import JSONDecodeError

# from itertools import chain
# from operator import methodcaller

import tornado.escape
import tornado.web
import tornado.websocket

from bs4 import BeautifulSoup
from tornado import httpclient

# from nltk.corpus import stopwords



class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('index.html')


class AnalyseURLHandler(tornado.websocket.WebSocketHandler):
    """
    Websocket handler

    TODO: look at reconnection strategies
    """


    # listen to any messages coming to socket
    async def on_message(self, message):
        logging.info("got message %r", message)

        # parse incoming JSON
        try:
            parsed = tornado.escape.json_decode(message)
        except JSONDecodeError as jde:
            return
        except TypeError as te:
            return

        # ignore any messages without a url
        if "url_for_wordcloud" not in parsed:
            return

        # TODO: validate url, ie protocol etc

        url_for_wordcloud = parsed["url_for_wordcloud"]
        http = httpclient.AsyncHTTPClient()

        # retrieve the URL asynchronously
        # include a User-Agent, as some servers dislike bots
        response = await http.fetch(url_for_wordcloud, headers={'User-Agent': 'Mozilla/5.0'})

        # get words from response body
        soup = BeautifulSoup(response.body, 'lxml')
        if soup:
            # get the title, and all paragraphs (ie ignore script tags etc
            text_tags = soup.body.find_all(['title', 'p'])
            words = ' '.join ([tag.string for tag in text_tags if tag.string is not None]).lower()

            # remove punctuation
            words = re.sub(r'[^\w\s]', '', words)

            # Try to count the words with a memory efficient iterables approach.
            # map(str.split, page_text) makes a list, items from which are chained together and then counted
            # TODO get this workig, not just making single characters
            # word_frequency_dict = Counter(chain.from_iterable(map(methodcaller("split", " "), words)))

            word_frequency_dict = Counter([word for word in words.split(' ')])

            print(word_frequency_dict)
            # remove articles and prepositions [stop words]
            # stop_words = stopwords.words('english')
            # word_frequency_dict = [word_frequency_dict.pop(k, None) for k in stopwords]

        # store
        return {'event': 'data'}


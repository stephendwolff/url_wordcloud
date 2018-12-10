# -*- coding: utf-8 -*-
import json
import logging
import os
import re
from collections import Counter
from json import JSONDecodeError

# from itertools import chain
# from operator import methodcaller

import tornado.escape
import tornado.web
import tornado.websocket
from tornado import httpclient

from bs4 import BeautifulSoup
from tornado_sqlalchemy import SessionMixin, as_future

# from nltk.corpus import stopwords
from url_wordcloud.models import Word

# use regular expression to remove common words
# could use nltk with more time
from url_wordcloud.utils import salted_hash, asymmetrically_encrypt

STOP_WORDS_PIPED = "i|me|my|myself|we|us|our|ours|ourselves|you|your|yours|yourself|yourselves|he|him|his|himself|she|her|hers|herself|it|its|itself|they|them|their|theirs|themselves|what|which|who|whom|whose|this|that|these|those|am|is|are|was|were|be|been|being|have|has|had|having|do|does|did|doing|will|would|should|can|could|ought|i'm|you're|he's|she's|it's|we're|they're|i've|you've|we've|they've|i'd|you'd|he'd|she'd|we'd|they'd|i'll|you'll|he'll|she'll|we'll|they'll|isn't|aren't|wasn't|weren't|hasn't|haven't|hadn't|doesn't|don't|didn't|won't|wouldn't|shan't|shouldn't|can't|cannot|couldn't|mustn't|let's|that's|who's|what's|here's|there's|when's|where's|why's|how's|a|an|the|and|but|if|or|because|as|until|while|of|at|by|for|with|about|against|between|into|through|during|before|after|above|below|to|from|up|upon|down|in|out|on|off|over|under|again|further|then|once|here|there|when|where|why|how|all|any|both|each|few|more|most|other|some|such|no|nor|not|only|own|same|so|than|too|very|say|says|said|shall"
STOP_WORDS = STOP_WORDS_PIPED.split('|')
STOP_WORDS_RE = re.compile(r'\b(' + r'|'.join(STOP_WORDS) + r')\b\s*')

URL_RE = re.compile(r'^((https?|ftp|smtp):\/\/)?(www.)?[a-z0-9]+\.[a-z]+(\/[a-zA-Z0-9#]+\/?)*')


class MainHandler(tornado.web.RequestHandler):
    """
    Homepage handler - for '/'
    """

    def get(self):
        """
        Render the homepage

        :return:
        """
        self.render('index.html')


class AnalyseURLHandler(SessionMixin, tornado.websocket.WebSocketHandler):
    """
    Websocket handler - for '/analyse_url/'
     - to receive URL
     - to return word frequency dictionary or error message

    TODO: look at reconnection strategies for websockets
    """
    pk = None

    def __init__(self, application, request, **kwargs):
        pk_path = os.path.join(os.path.dirname(__file__), "..", "..", "public_key")

        with open(pk_path, 'rb') as f:
            self.pk = f.read()

        super(AnalyseURLHandler, self).__init__(application, request, **kwargs)

    async def on_message(self, message):
        """
        Listen to any messages coming to socket and use url_for_wordcloud parameter if provided
        to retrieve webpage, and analyse word count

        TODO: split up on_message into smaller functional parts and add tests

        :param message:
        :return: word frequency dict, or error message
        """
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

        url_for_wordcloud = parsed["url_for_wordcloud"]
        logging.info("url_for_wordcloud %r", url_for_wordcloud)

        if not re.match(URL_RE, url_for_wordcloud):
            logging.info('invalid URL')

            # write_error available, with HTTP status codes, not sure with websockets
            self.write_message(json.dumps({
                'error': 'invalid URL'
            }))
            return

        if not (url_for_wordcloud.startswith('http://') or url_for_wordcloud.startswith('https://')):
            # assume upgrade to https if available
            url_for_wordcloud = "{0}".format('http://', url_for_wordcloud)

        # retrieve the URL asynchronously
        # include a User-Agent, as some servers dislike bots
        http = httpclient.AsyncHTTPClient()
        try:
            response = await http.fetch(url_for_wordcloud, headers={'User-Agent': 'Mozilla/5.0'})
        except Exception as e:
            logging.error(e)
            self.write_message(json.dumps({
                'error': 'exception {0}'.format(e)
            }))
            return

        # get words from response body
        soup = BeautifulSoup(response.body, 'lxml')
        [s.extract() for s in soup('script')]
        word_frequency_dict = {}

        # remove script, style and iframe tags
        for script in soup(["script", "style", "iframe"]):
            script.decompose()  # rip it out

        # get text
        if soup:
            # to lower case
            words = soup.get_text().lower()

            # remove punctuation
            words = re.sub(r'[^\w\s]', '', words)

            # remove line breaks
            words = re.sub(r"\n|\r", " ", words)

            # remove double spaces
            words = re.sub(' +', ' ', words)

            # remove stop words (leaving nouns and verbs)
            # stop words above could be retrieved from ntlk
            words = re.sub(STOP_WORDS_RE, '', words)
            # stop_words = stopwords.words('english')
            # word_frequency_dict = [word_frequency_dict.pop(k, None) for k in stopwords]

            logging.info("words %r", words)

            # split up the string into words, and count how often the occur
            word_frequency_dict = Counter([word for word in words.split(' ')])

            # store the top 100
            top_hundred = word_frequency_dict.most_common(100)
            logging.info("top_hundred %r", top_hundred)

            with self.make_session() as session:
                words = []

                for word, frequency in top_hundred:
                    pk = salted_hash(word)
                    encrypted_word = asymmetrically_encrypt(word, self.pk)

                    # get word from db in non-blocking fashion
                    db_word = await as_future(session.query(Word).filter_by(pk=pk).first)

                    if db_word is not None:
                        # update
                        db_word.frequency = frequency
                        words.append(db_word)
                    else:
                        # insert
                        new_word = Word(
                            pk=pk,
                            word=encrypted_word,
                            frequency=frequency)
                        words.append(new_word)
                    # maybe simpler way to do this with SQLAlchemy merge,
                    # but i'm not very familiar with SQLAlchemy

                    # session.merge(new_word, load=True)

                # check whether this makes any db calls?
                # i think it just updates the sqlalchemy session
                session.add_all(words)

                # not sure whether i need to make this async, but it should make db calls which are blocking
                # await as_future(session.commit())
                session.commit()

            word_frequency_json = json.dumps(word_frequency_dict)

            self.write_message(word_frequency_json)
        else:
            logging.info('No words found')
            # write_error available, with HTTP status codes, not sure with websockets
            self.write_message(json.dumps({
                'error': "No words found"
            }))

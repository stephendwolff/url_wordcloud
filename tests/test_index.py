import tornado

from tornado.testing import AsyncTestCase, AsyncHTTPTestCase

from url_wordcloud.utils import generate_keys
from .mixins import HTTPClientMixin
from url_wordcloud.app import URLWordCloudApplication


class IndexTestCase(AsyncHTTPTestCase, HTTPClientMixin):

    def get_app(self):
        generate_keys()

        # TODO get parameters from app cmd line options
        return URLWordCloudApplication("root", "root", "mysql", "test_urlwordcloud")

    @tornado.testing.gen_test
    def test_home(self):
        response = yield self.get('/')
        self.assertTrue(b'URL WORDCLOUD' in response.body)

    @tornado.testing.gen_test
    def test_admin(self):
        response = yield self.get('/admin/')
        self.assertTrue('login' in response.effective_url)

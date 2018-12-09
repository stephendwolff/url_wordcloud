import tornado

from tornado.httpclient import AsyncHTTPClient
from tornado.testing import AsyncTestCase, AsyncHTTPTestCase

from .mixins import HTTPClientMixin
from url_wordcloud.app import URLWordCloudApplication


class IndexTestCase(AsyncHTTPTestCase, HTTPClientMixin):

    def get_app(self):
        return URLWordCloudApplication()

    @tornado.testing.gen_test
    def test_home(self):
        response = yield self.get('/')
        self.assertTrue(b'URL WORDCLOUD' in response.body)

    @tornado.testing.gen_test
    def test_admin(self):
        response = yield self.get('/admin/')

        # test going straight to admin re-directs to login
        self.assertTrue('login' in response.effective_url)


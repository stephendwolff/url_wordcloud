import tornado

from tornado.httpclient import AsyncHTTPClient
from tornado.testing import AsyncTestCase


# This test uses coroutine style.
class MyTestCase(AsyncTestCase):
    @tornado.testing.gen_test
    def test_http_fetch(self):
        client = AsyncHTTPClient()
        response = yield client.fetch("http://localhost:8888/")
        # Test contents of response
        self.assertIn(b"Boilerplate", response.body)


# This test uses argument passing between self.stop and self.wait.
class MyTestCase2(AsyncTestCase):
    def test_http_fetch(self):
        client = AsyncHTTPClient()
        client.fetch("http://localhost:8888/", self.stop)
        response = self.wait()
        # Test contents of response
        self.assertIn(b"Boilerplate", response.body)
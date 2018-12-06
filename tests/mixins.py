from urllib.parse import urlencode

# mixin for handy testing
# https://www.peterbe.com/plog/tricks-asynchttpclient-tornado
from url_wordcloud.app import URLWordCloudApplication


class HTTPClientMixin(object):

   def get(self, url, data=None, headers=None):
       if data is not None:
           if isinstance(data, dict):
               data = urlencode(data)
           if '?' in url:
               url += '&amp;%s' % data
           else:
               url += '?%s' % data
       return self._fetch(url, 'GET', headers=headers)

   def post(self, url, data, headers=None):
       if data is not None:
           if isinstance(data, dict):
               data = urlencode(data)
       return self._fetch(url, 'POST', data, headers)

   async def _fetch(self, url, method, data=None, headers=None):
       response = await self.http_client.fetch(self.get_url(url), self.stop, method=method,
                              body=data, headers=headers)
       return response #self.wait()

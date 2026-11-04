from w3lib.http import basic_auth_header


class ProxyMiddleware:

    def __init__(self, crawler):
        self._auth = None
        self._proxy = None
        self.__spider = crawler.spider

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request):
        if self._proxy is None:
            self._proxy = self.__spider.proxy
            self._auth = basic_auth_header(self._proxy.username, self._proxy.password)

        request.meta["proxy"] = self._proxy.get_proxy()
        request.headers["Proxy-Authorization"] = self._auth

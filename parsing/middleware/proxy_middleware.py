from w3lib.http import basic_auth_header


class ProxyMiddleware:

    def __init__(self):
        self._auth = None
        self._proxy = None

    def process_request(self, request, spider):
        if self._proxy is None:
            self._proxy = spider.proxy
            self._auth = basic_auth_header(self._proxy.username, self._proxy.password)

        request.meta["proxy"] = self._proxy.get_proxy()
        request.headers["Proxy-Authorization"] = self._auth

from typing import Self
from w3lib.http import basic_auth_header


class ProxyMiddleware:

    def __init__(self, crawler):
        self.__auth = None
        self.__proxy = None
        self.__spider = crawler.spider

    @classmethod
    def from_crawler(cls, crawler) -> Self:
        return cls(crawler)

    def process_request(self, request) -> None:
        if self.__proxy is None:
            self.__proxy = self.__spider.proxy
            self.__auth = basic_auth_header(self.__proxy.username, self.__proxy.password)

        request.meta["proxy"] = self.__proxy.get_proxy()
        request.headers["Proxy-Authorization"] = self.__auth

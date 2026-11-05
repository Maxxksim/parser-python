import random

from config.proxy_config import ProxyConfig


class Proxy:

    def __init__(self, config: ProxyConfig):
        self.__config = config
        self.__proxy_list = None
        self.__last_proxy = None

    def get_proxy(self) -> str:
        """
        Take random proxy from proxy list and
        save last proxy.

        :return: one random proxy from list
        """

        if not self.__proxy_list:
            self.__proxy_list = self.__config.proxy_list.copy()
            random.shuffle(self.__proxy_list)

            if len(self.__proxy_list) > 0 and self.__proxy_list[len(self.__proxy_list) - 1] == self.__last_proxy:
                self.__proxy_list.insert(0, self.__proxy_list.pop())

        self.__last_proxy = self.__proxy_list.pop()
        return self.__last_proxy

    @property
    def username(self) -> str:
        return self.__config.proxy_username

    @property
    def password(self) -> str:
        return self.__config.proxy_password

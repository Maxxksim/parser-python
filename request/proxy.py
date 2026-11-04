from config.proxy_config import ProxyConfig


class Proxy:

    def __init__(self, config: ProxyConfig):
        self.__username = config.proxy_username
        self.__password = config.proxy_password
        self.__proxy_list = config.proxy_list
        self.__index_next_proxy = 0

    def get_proxy(self) -> None:
        if self.__index_next_proxy + 1 > len(self.__proxy_list):
            self.__index_next_proxy = 0

        proxy = self.__proxy_list[self.__index_next_proxy]
        self.__index_next_proxy += 1

        return proxy

    @property
    def username(self) -> str:
        return self.__username

    @property
    def password(self) -> str:
        return self.__password

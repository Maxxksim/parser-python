from config.proxy_config import ProxyConfig


class Proxy:

    def __init__(self, config: ProxyConfig):
        self._username = config.proxy_username
        self._password = config.proxy_password
        self._proxy_list = config.proxy_list
        self._index_next_proxy = 0

    def get_proxy(self):
        if self._index_next_proxy + 1 > len(self._proxy_list):
            self._index_next_proxy = 0

        proxy = self._proxy_list[self._index_next_proxy]
        self._index_next_proxy += 1

        return proxy

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

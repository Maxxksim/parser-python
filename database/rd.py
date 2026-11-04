from config.redis_config import RedisConfig
import redis


class Rd:
    def __init__(self, config: RedisConfig):
        self.__url = config.url

    def get_client(self):
        return redis.Redis.from_url(self.__url, socket_timeout=40)
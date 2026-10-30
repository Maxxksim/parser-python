from config.redis_config import RedisConfig
import redis


class Rd:
    def __init__(self, config: RedisConfig):
        self.url = config.url

    def get_client(self):
        return redis.Redis.from_url(self.url)
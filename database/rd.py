from config.redis_config import RedisConfig
import redis
from redis import Redis
from redis.maint_notifications import MaintNotificationsConfig


class Rd:
    def __init__(self, config: RedisConfig):
        self.__url = config.url

    def get_client(self) -> Redis:
        """
        Make connection to Redis.

        :return: connection of Redis
        """
        return redis.Redis.from_url(self.__url, socket_timeout=40, maint_notifications_config=MaintNotificationsConfig(enabled=False))
from config.database_config import DbConfig
from config.queue_config import QueueConfig
from config.redis_config import RedisConfig


class Config:

    def __init__(self):
        self._queue = QueueConfig()
        self._db = DbConfig()
        self._redis = RedisConfig()

    @property
    def queue(self):
        return self._queue

    @property
    def db(self):
        return self._db

    @property
    def redis(self):
        return self._redis
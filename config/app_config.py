from config.database_config import DbConfig
from config.logger_config import LoggerConfig
from config.proxy_config import ProxyConfig
from config.queue_config import QueueConfig
from config.redis_config import RedisConfig


class Config:

    def __init__(self):
        self.__queue = QueueConfig()
        self.__db = DbConfig()
        self.__redis = RedisConfig()
        self.__proxy = ProxyConfig()
        self.__logger = LoggerConfig()

    @property
    def queue(self):
        return self.__queue

    @property
    def db(self):
        return self.__db

    @property
    def redis(self):
        return self.__redis

    @property
    def proxy(self):
        return self.__proxy

    @property
    def logger(self):
        return self.__logger
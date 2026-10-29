from config.database_config import DbConfig
from config.queue_config import QueueConfig


class Config:

    def __init__(self):
        self._queue = QueueConfig()
        self._db = DbConfig()

    @property
    def queue(self):
        return self._queue

    @property
    def db(self):
        return self._db
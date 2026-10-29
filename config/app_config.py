from config.queue_config import QueueConfig


class Config:

    def __init__(self):
        self._queue = QueueConfig()

    @property
    def queue(self):
        return self._queue

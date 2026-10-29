from config.app_config import Config
from queues.app_queue import Queue

config = Config()
queue = Queue(config)
queue.start()


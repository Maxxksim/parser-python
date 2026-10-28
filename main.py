from Config.Config import Config
from Queue.queue import Queue

config = Config()
queue = Queue(config)
queue.start()
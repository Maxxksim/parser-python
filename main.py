from config.app_config import Config
from database.db import Db
from queues.app_queue import Queue

config = Config()
db = Db(config.db)
queue = Queue(config.queue)
queue.start()


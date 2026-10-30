from config.app_config import Config
from database.db import Db
from database.rd import Rd
from parsing.parser import Parser
from queues.app_queue import Queue

config = Config()
db = Db(config.db)
redis = Rd(config.redis)
parser = Parser(redis)
queue = Queue(config.queue, parser, redis)
queue.start()



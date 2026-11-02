from config.app_config import Config
from controller.parsed_data_controller import ParsedDataController
from database.db import Db
from database.rd import Rd
from parsing.parser import Parser
from queues.app_queue import Queue
from request.proxy import Proxy

config = Config()
db = Db(config.db)
redis = Rd(config.redis)
proxy = Proxy(config.proxy)
parser = Parser(redis, proxy)
controller = ParsedDataController(db)
queue = Queue(config.queue, parser, redis, controller)
queue.start()
parser.parse()

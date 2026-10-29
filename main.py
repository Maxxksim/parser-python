from scrapy.crawler import CrawlerProcess

from config.app_config import Config
from database.db import Db
from parsing.parser import Parser
from queues.app_queue import Queue

config = Config()
db = Db(config.db)
queue = Queue(config.queue)
#queue.start()

process = CrawlerProcess(settings={
        "FEEDS": {"links.json": {"format": "json", "overwrite": True}},
    })
process.crawl(Parser)
process.start()


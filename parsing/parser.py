from scrapy.crawler import CrawlerProcess
from database.rd import Rd
from parsing.pipelines.collect_parsed_data_pipeline import CollectParsedDataPipeline
from parsing.spiders.parse_links_spider import ParseLinksSpider
from parsing.pipelines.fill_queue_pipeline import FillQueuePipeline
from parsing.spiders.parse_qa_spider import ParseQA

BASE_URL = 'https://www.kreuzwort-raetsel.net/'
NOT_FOUND_QUESTION = 'Die Suche hat leider keine Ergebnisse.'


class Parser:

    def __init__(self, redis: Rd):
        self._redis = redis
        #self.fill_queue()

    def fill_queue(self):
        self.__run_spider({
            "ITEM_PIPELINES": {FillQueuePipeline: 100},
            "REDIS": self._redis
        },
            ParseLinksSpider,
        )

    def __run_spider(self, settings: dict, spider, **kwargs):
        process = CrawlerProcess(settings=settings)
        process.crawl(spider, **kwargs)
        process.start()

    def parse(self, link: str):
        self.__run_spider({
            "ITEM_PIPELINES": {CollectParsedDataPipeline: 100},
            "REDIS": self._redis
        },
            ParseQA,
            link=link)

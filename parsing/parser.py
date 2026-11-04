from scrapy.crawler import CrawlerProcess
from database.rd import Rd
from parsing.middleware.proxy_middleware import ProxyMiddleware
from parsing.pipelines.collect_parsed_data_pipeline import CollectParsedDataPipeline
from parsing.spiders.parse_links_spider import ParseLinksSpider
from parsing.pipelines.fill_queue_pipeline import FillQueuePipeline
from parsing.spiders.parse_qa_spider import ParseQA
from request.proxy import Proxy


class Parser:

    def __init__(self, redis: Rd, proxy: Proxy):
        self._redis = redis
        self._proxy = proxy

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

    def start_parsing_links(self):
        self.__run_spider({
            "ITEM_PIPELINES": {CollectParsedDataPipeline: 100},
            "DOWNLOADER_MIDDLEWARES": {ProxyMiddleware: 100},
        },
            ParseQA,
            redis=self._redis,
            proxy=self._proxy,
        )

    def get_new_instance(self) -> "Parser":
        return type(self)(self._redis, self._proxy)
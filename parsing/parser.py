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
        self.__redis = redis
        self.__proxy = proxy

    def fill_queue(self):
        self.__run_spider({
            "ITEM_PIPELINES": {FillQueuePipeline: 100},
            "REDIS": self.__redis
        },
            ParseLinksSpider,
        )

    def __run_spider(self, settings: dict, spider, **kwargs) -> None:
        process = CrawlerProcess(settings=settings)
        process.crawl(spider, **kwargs)
        process.start()

    def start_parsing_links(self) -> None:
        self.__run_spider({
            "ITEM_PIPELINES": {CollectParsedDataPipeline: 100},
            "DOWNLOADER_MIDDLEWARES": {ProxyMiddleware: 100},
        },
            ParseQA,
            redis=self.__redis,
            proxy=self.__proxy,
        )

    def get_new_instance(self) -> "Parser":
        return type(self)(self.__redis, self.__proxy)
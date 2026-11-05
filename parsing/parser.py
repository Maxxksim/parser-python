from Logs.logger import Logger
from scrapy.crawler import CrawlerProcess
from database.rd import Rd
from parsing.middleware.proxy_middleware import ProxyMiddleware
from parsing.pipelines.collect_parsed_data_pipeline import CollectParsedDataPipeline
from parsing.spiders.parse_links_spider import ParseLinksSpider
from parsing.pipelines.fill_queue_pipeline import FillQueuePipeline
from parsing.spiders.parse_qa_spider import ParseQA
from request.proxy import Proxy


class Parser:

    def __init__(self, redis: Rd, proxy: Proxy, logger: Logger):
        self.__redis = redis
        self.__proxy = proxy
        self.__logger = logger

    def fill_queue(self):
        self.__run_spider({
            "ITEM_PIPELINES": {FillQueuePipeline: 100},
            "REDIS": self.__redis,
            "DOWNLOADER_MIDDLEWARES": {ProxyMiddleware: 100},
        },
            ParseLinksSpider,
            proxy=self.__proxy
        )

    def __run_spider(self, settings: dict, spider, **kwargs) -> None:
        process = CrawlerProcess(settings={**settings, **self.__default_settings})
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
            logger=self.__logger,
        )

    def get_new_instance(self) -> "Parser":
        return type(self)(self.__redis, self.__proxy, self.__logger)

    def __define_log_mode(self) -> str | None:
        if self.__logger.log_mode == 'file':
            return self.__logger.logs_path

        return None

    @property
    def __default_settings(self):
        return {
            "LOG_FILE": self.__define_log_mode()
        }

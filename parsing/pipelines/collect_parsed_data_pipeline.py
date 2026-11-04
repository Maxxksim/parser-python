import json
from collections import defaultdict


class CollectParsedDataPipeline:

    def __init__(self, crawler):
        self.crawler = crawler

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def close_spider(self) -> None:
        self.crawler.spider.redis_client.close()

    def process_item(self, item) -> dict:
        spider = self.crawler.spider

        if item["link"] == spider.link:
            spider.collected_data[item["question"]] = item["answers"]
        return item

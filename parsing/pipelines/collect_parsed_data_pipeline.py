from typing import Self


class CollectParsedDataPipeline:

    def __init__(self, crawler):
        self.__spider = crawler.spider

    @classmethod
    def from_crawler(cls, crawler) -> Self:
        return cls(crawler)

    def close_spider(self) -> None:
        self.__spider.redis_client.close()

    def process_item(self, item) -> dict:
        if item["link"] == self.__spider.link:
            self.__spider.collected_data[item["question"]] = item["answers"]
        return item

from typing import Self


class CollectParsedDataPipeline:

    def __init__(self, crawler):
        self.__spider = crawler.spider

    @classmethod
    def from_crawler(cls, crawler) -> Self:
        """
        Getting transferred data from spider.

        :param crawler:
        :return: instance of itself
        """
        return cls(crawler)

    def close_spider(self) -> None:
        """
        Close Redis connection.

        :return: None
        """
        self.__spider.redis_client.close()

    def process_item(self, item) -> dict:
        """
        Collect data from one page.

        :param item:
        :return: dict with question and its answers
        """
        if item["link"] == self.__spider.link:
            self.__spider.collected_data[item["question"]] = item["answers"]
        return item

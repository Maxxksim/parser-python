from typing import Any, Self
from database.rd import Rd


class FillQueuePipeline:

    def __init__(self, redis: Rd):
        self.__redis_client = redis.get_client()

    @classmethod
    def from_crawler(cls, crawler) -> Self:
        return cls(
            redis=crawler.settings.get("REDIS"),
        )

    def close_spider(self, spider) -> None:
        self.__redis_client.close()

    def process_item(self, item) -> dict[str, Any]:
        new_links = self.__get_only_new_link(item["links"])

        if new_links:
            self.__redis_client.lpush("queue", *new_links)
            self.__redis_client.sadd("set:processing:links", *new_links)
        return item

    def __get_only_new_link(self, links: list) -> list[str]:

        if not links:
            return []

        result_parsed_check = self.__redis_client.smismember("set:parsed:links", links)
        result_processing_check = self.__redis_client.smismember("set:processing:links", links)
        new_links = []

        for url, parsed, processing in zip(links, result_parsed_check, result_processing_check):
            if not parsed and not processing:
                new_links.append(url)

        return new_links

from database.rd import Rd


class FillQueuePipeline:

    def __init__(self, redis: Rd):
        self.redis = redis

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            redis=crawler.settings.get("REDIS"),
        )

    def open_spider(self, spider):
        self.redis_client = self.redis.get_client()

    def close_spider(self, spider):
        self.redis_client.close()

    def process_item(self, item, spider):
        urls = item["urls"]
        result_check = self.redis_client.smismember("set:parsed:links", urls)

        for url, parsed in zip(urls, result_check):
            if not parsed:
                self.redis_client.lpush("queue", url)

        self.redis_client.lpush("queue", *item["urls"])
        return item

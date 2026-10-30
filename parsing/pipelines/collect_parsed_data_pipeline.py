import json
from collections import defaultdict

from database.rd import Rd


class CollectParsedDataPipeline:

    def __init__(self, redis: Rd):
        self.collectedData = defaultdict(list)
        self.redis = redis

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            redis=crawler.settings.get("REDIS"),
        )

    def open_spider(self, spider):
        self.redis_client = self.redis.get_client()

    def close_spider(self, spider):
        link = next(iter(self.collectedData))
        self.redis_client.lpush('queue:parsed:data', json.dumps(self.collectedData))
        self.redis_client.sadd('set:parsed:links', link)
        self.redis_client.close()

    def process_item(self, item, spider):
        self.collectedData[item['link']].append({
            "question": item['question'],
            "answers": item['answers'],
        })

        return item

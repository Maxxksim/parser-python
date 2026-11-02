import json
from collections import defaultdict

from database.rd import Rd


class CollectParsedDataPipeline:

    def __init__(self):
        self.collectedData = defaultdict(list)

    def close_spider(self, spider):
        link = next(iter(self.collectedData))
        spider.redis_client.lpush('queue:parsed:data', json.dumps(self.collectedData))
        spider.redis_client.sadd('set:parsed:links', link)
        spider.redis_client.close()

    def process_item(self, item, spider):
        self.collectedData[item['link']].append({
            "question": item['question'],
            "answers": item['answers'],
        })

        return item

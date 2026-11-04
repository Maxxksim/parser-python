from urllib.parse import quote
from scrapy import Request, signals
from scrapy.exceptions import DontCloseSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.settings.default_settings import DOWNLOAD_DELAY, AUTOTHROTTLE_ENABLED
from scrapy.spiders import CrawlSpider, Rule
from database.rd import Rd


class ParseQA(CrawlSpider):
    name = "PARSE QUESTIONS & ANSWERS SPIDER"
    BASE_URL = 'https://www.kreuzwort-raetsel.net/'
    NOT_FOUND_QUESTION = 'Die Suche hat leider keine Ergebnisse.'
    handle_httpstatus_list = [404]
    MAX_ATTEMPTS = 3
    custom_settings = {
        DOWNLOAD_DELAY : 3,
        AUTOTHROTTLE_ENABLED : True
    }

    def __init__(self, redis: Rd, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.redis_client = redis.get_client()
        self.link = None

    rules = (
        Rule(
            LinkExtractor(restrict_css="table:not(#kxo) tr td.Question"),
            callback="parse_item",
            errback='handle_error',
            follow=False,
        ),
    )

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_idle, signal=signals.spider_idle)
        return spider

    async def parse_item(self, response):
        question = response.meta.get("link_text")

        if response.status == 404 or response.css('span[data-lf="more"]:not([hidden])'):
            answers = await self.make_searching_question(question)
        else:
            answers = self.get_answers_with_lengths(response)

        if answers:
            yield self.parsed_item(question, answers)

    def parsed_item(self, question, answers):
        return {"question": question, "answers": answers, "link": self.link}

    def spider_idle(self):
        link = self.redis_client.lmove(
            'queue', 'queue:processing', src='RIGHT', dest='LEFT',
        )

        if link is None:
            return

        self.link = link.decode()

        self.crawler.engine.crawl(Request(link.decode()))
        raise DontCloseSpider

    @staticmethod
    def make_url_to_search_question(question):
        return f"https://www.kreuzwort-raetsel.net/suche.php?s={quote(question, safe='')}&field=0&go=suchen#suchbox"

    @staticmethod
    def get_answers_with_lengths(response, question_for_comparing=None):
        result = []

        for tr in response.css("tr"):
            answer = tr.css("td.Answer ::text").getall()

            if not answer:
                continue

            if question_for_comparing is not None:
                question = tr.css("td.Question a::text").get()

                if question != question_for_comparing:
                    continue

            result.append({
                "answer": answer,
                "length": tr.css("td.Length::text").get().strip(),
            })
        return result

    async def make_searching_question(self, question):
        response = await self.crawler.engine.download_async(
            Request(self.make_url_to_search_question(question))
        )

        searched_result = response.css("form div#SearchresultsCounter strong::text").get()

        if searched_result is None or searched_result == self.NOT_FOUND_QUESTION:
            return None

        answers = []

        while True:
            answers.extend(self.get_answers_with_lengths(response, question))

            next_url = response.css("tfoot td ul.Pagination li.Next a::attr(href)").get()

            if not next_url:
                break

            request = Request(response.urljoin(next_url), dont_filter=True)
            response = await self.crawler.engine.download_async(request)

        return answers

    def handle_error(self, failure):
        link = failure.request.url
        attempt = self.redis_client.hincrby('queue:attempts', link, 1)
        pipe = self.redis_client.pipeline(transaction=True)

        if attempt >= self.MAX_ATTEMPTS:
            pipe.sadd("set:failed:links", link)
            pipe.lrem("queue:processing", 1, link)
            pipe.srem("set:processing", link)
            pipe.hdel("queue:attempts", link)
        else:
            pipe.redis_client.lpush('queue', link)
            pipe.redis_client.lrem('queue:processing', 1 , link)

        pipe.execute()
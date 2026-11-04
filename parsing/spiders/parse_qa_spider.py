import os
from collections import defaultdict
from typing import AsyncGenerator, Self
from urllib.parse import quote

from Logs.logger import Logger
from scrapy import Request, signals
from scrapy.exceptions import DontCloseSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule, Spider
from twisted.python.failure import Failure

from database.rd import Rd
import json


class ParseQA(CrawlSpider):
    name = "PARSE QUESTIONS & ANSWERS SPIDER"
    BASE_URL = 'https://www.kreuzwort-raetsel.net/'
    NOT_FOUND_QUESTION = 'Die Suche hat leider keine Ergebnisse.'
    handle_httpstatus_list = [404]
    MAX_ATTEMPTS = 3
    custom_settings = {
        "DOWNLOAD_DELAY": 3,
        "AUTOTHROTTLE_ENABLED": True,
        "TELNETCONSOLE_ENABLED": False,
    }

    def __init__(self, redis: Rd, logger: Logger, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.redis_client = redis.get_client()
        self.link = None
        self.collected_data = defaultdict(dict)
        self.__logger = logger

    rules = (
        Rule(
            LinkExtractor(restrict_css="table:not(#kxo) tr td.Question"),
            callback="parse_item",
            errback="__handle_error",
            follow=False,
        ),
    )

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_idle, signal=signals.spider_idle)
        return spider

    async def parse_item(self, response) -> AsyncGenerator[dict]:
        question = response.meta.get("link_text")

        if response.status == 404 or response.css('span[data-lf="more"]:not([hidden])'):
            answers = await self.__make_searching_question(question)
        else:
            answers = self.__get_answers_with_lengths(response)

        yield self.parsed_item(question, answers)

    def parsed_item(self, question, answers):
        return {"question": question, "answers": answers, "link": self.link}

    def __add_parsed_data(self) -> None:
        if self.link is None:
            return
        pipe = self.redis_client.pipeline(transaction=True)
        pipe.lpush("queue:parsed:data", json.dumps({self.link: self.collected_data}))
        pipe.sadd("set:parsed:links", self.link)
        pipe.execute()
        self.__logger.log.info(
            "PARSER MESSAGE (PARSING): process %s started parsing link: %s.",
            os.getppid(),
            self.link,
        )
        self.link = None
        self.collected_data.clear()

    def spider_idle(self):
        self.__add_parsed_data()
        link = self.redis_client.lmove(
            'queue', 'queue:processing', src='RIGHT', dest='LEFT',
        )

        if link is None:
            self.__logger.log.info("QUEUE MESSAGE (PARSING): Queue is empty.")
            return

        self.__logger.log.info(
            "PARSER MESSAGE (PARSING): process %s started parsing link: %s.",
            os.getppid(),
            link.decode(),
        )
        self.link = link.decode()

        self.crawler.engine.crawl(Request(self.link, errback=self.__handle_error, dont_filter=True))
        raise DontCloseSpider

    @staticmethod
    def __make_url_to_search_question(question) -> str:
        return f"https://www.kreuzwort-raetsel.net/suche.php?s={quote(question, safe='')}&field=0&go=suchen#suchbox"

    @staticmethod
    def __get_answers_with_lengths(response, question_for_comparing=None) -> list[str]:
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

    async def __make_searching_question(self, question) -> list[str] | None:
        response = await self.crawler.engine.download_async(
            Request(self.__make_url_to_search_question(question))
        )

        searched_result = response.css("form div#SearchresultsCounter strong::text").get()

        if searched_result is None or searched_result == self.NOT_FOUND_QUESTION:
            return None

        answers = []

        while True:
            answers.extend(self.__get_answers_with_lengths(response, question))

            next_url = response.css("tfoot td ul.Pagination li.Next a::attr(href)").get()

            if not next_url:
                break

            request = Request(response.urljoin(next_url), dont_filter=True)
            response = await self.crawler.engine.download_async(request)

        return answers

    def __handle_error(self, failure: Failure) -> None:
        link = self.link

        if link is None:
            return
        self.link = None
        self.collected_data.clear()
        attempt = self.redis_client.hincrby('queue:attempts', link, 1)
        pipe = self.redis_client.pipeline(transaction=True)

        if attempt >= self.MAX_ATTEMPTS:
            pipe.sadd("set:failed:links", link)
            pipe.lrem("queue:processing", 1, link)
            pipe.srem("set:processing", link)
            pipe.hdel("queue:attempts", link)
            self.__logger.log.error(
                "PARSER MESSAGE (PARSING): Error: link %s haven\'t been parsed after %s attempts.",
                link,
                self.MAX_ATTEMPTS,
            )
        else:
            pipe.lpush('queue', link)
            pipe.lrem('queue:processing', 1, link)

        pipe.execute()

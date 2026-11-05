from typing import Any, Generator

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class ParseLinksSpider(CrawlSpider):
    START_URL = "https://www.kreuzwort-raetsel.net/uebersicht.html"
    name = "PARSE LINKS SPIDER"
    allowed_domains = ["www.kreuzwort-raetsel.net"]
    start_urls = [START_URL]

    rules = (
        Rule(LinkExtractor(restrict_css='ul.dnrg'), callback='parse_item', follow=False),
    )

    @staticmethod
    def parse_item(response) -> Generator[dict[str, list[Any]], Any, None]:
        """
        Make parsing of links each contains a page where are located questions.

        :param response:
        :return: generator of dicts each with parsed links
        """
        hrefs = response.css('ul.dnrg li a::attr(href)').getall()
        yield {"links": [response.urljoin(href) for href in hrefs]}

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class ParseLinksSpider(CrawlSpider):
    START_URL = "https://www.kreuzwort-raetsel.net/uebersicht.html"
    name = "PARSE LINKS SPIDER"
    allowed_domains = ["www.kreuzwort-raetsel.net"]
    start_urls = [START_URL]
    custom_settings = {'DOWNLOAD_DELAY': 3}

    rules = (
        Rule(LinkExtractor(restrict_css='ul.dnrg'), callback='parse_item', follow=False),
    )

    @staticmethod
    def parse_item(response):
        hrefs = response.css('ul.dnrg li a::attr(href)').getall()
        yield {"urls": [response.urljoin(href) for href in hrefs]}

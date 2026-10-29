from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class Parser(CrawlSpider):
    name = "www.kreuzwort-raetsel.net"
    allowed_domains = ["www.kreuzwort-raetsel.net"]
    start_urls = ['https://www.kreuzwort-raetsel.net/uebersicht.html']
    custom_settings = {'DOWNLOAD_DELAY': 3}

    rules = (
        Rule(LinkExtractor(restrict_css='ul.dnrg'), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        for href in response.css('ul.dnrg li a::attr(href)').getall():
            yield {'url': response.urljoin(href)}

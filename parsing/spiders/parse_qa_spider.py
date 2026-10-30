from urllib.parse import quote
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class ParseQA(CrawlSpider):
    name = "PARSE QUESTIONS & ANSWERS SPIDER"
    BASE_URL = 'https://www.kreuzwort-raetsel.net/'

    def __init__(self, link=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.link = link
        self.start_urls = [link]

    rules = (
        Rule(LinkExtractor(restrict_css='table:not(#kxo) tbody')),
        Rule(LinkExtractor(restrict_css='table#kxo tbody'), callback="parse_item", follow=False)
    )

    def parse_item(self, response):
        question = response.meta.get("link_text").strip()
        answers = []
        for tr in response.css("table#kxo tbody tr"):
            answers.append({
                "answer": tr.css("td.Answer::text").get().strip(),
                "length": tr.css("td.Length::text").get().strip(),
            })

        yield {
            "question": question,
            "answers": answers,
            "link": self.link
        }

    @staticmethod
    def make_url_to_search_question(question):
        return f"https://www.kreuzwort-raetsel.net/suche.php?s={quote(question)}&field=0&go=suchen#suchbox"

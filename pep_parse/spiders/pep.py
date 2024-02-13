import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        for link in response.css('#numerical-index a.pep::attr(href)'):
            yield response.follow(link, callback=self.parse_pep)

    def parse_pep(self, response):
        yield PepParseItem(
            number=response.css(
                '#pep-content h1::text'
            ).get().split('-')[0].split()[1].strip(),
            name=response.css(
                '#pep-content h1::text').get().split('–')[1].strip(),
            status=response.css('abbr::text').get(),
        )

import scrapy

from pep_parse.items import PepParseItem

DOMAIN = 'peps.python.org'


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = [DOMAIN]
    start_urls = ['https://' + f'{domain}/' for domain in allowed_domains]

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

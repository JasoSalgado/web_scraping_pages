"""
Extract title from two pages, which are inside of a iframe
"""

# Modules
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy import Request


class Dummy(Item):
    title = Field()
    title_iframe = Field()


def parse_iframe(response):
    item = ItemLoader(Dummy(), response)
    item.add_xpath('titulo_iframe', '//div[@id="main"]//h1/span/text()')
    item.add_value('title', response.meta.get('title'))

    yield item.load_item()


class W3SCrawler(CrawlSpider):
    name = 'w3s'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
        'REDIRECT_ENABLED': True  # Parametro para activar los redirects (codigo 302)
    }

    allowed_domains = ['w3school.com']

    start_urls = ['https://www.w3schools.com/html/html_iframe.asp']
    download_delay = 1

    def parse(self, response):
        sel = Selector(response)

        title = sel.xpath('//div[@id="main"]//h1/span/text()').get()
        previous_data = {
            'title': title
        }

        iframe_url = "https://www.w3schools.com/html/" + iframe_url

        yield Request(
            iframe_url,  # iframe´s urls
            callback=parse_iframe,  # function inside the class that is going to process the iframe
            meta=previous_data
        )

from scrapy.item import Field, Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup

# Abstraction of data to get
class News(Item):
    id = Field()
    title = Field()
    description = Field()


# Class core - spider
class UniversoSpider(Spider):
    name = 'UniversoSpider'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36'
    }
    start_urls = ['https://www.eluniverso.com/deportes']

    def parse(self, response):
        selec = Selector(response)
        news = selec.xpath('//div[@class="view-content"]/div[@class="posts"]')
        for i, elem in enumerate(news):
            item = ItemLoader(News(), elem)

            # Filling the item with xpath expressions
            item.add_xpath('title', './/h2/a/text()')
            item.add_xpath('description', './/text()')
            item.add_value('id', i)

            # We return our filled item
            yield item.load_item()
from scrapy.item import Field, Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup

class Drugstore(Item):
    name = Field()
    price = Field()

class CruzVerde(CrawlSpider):
    name = 'Drugstore'
    custom_settings = {

        'USER-AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/80.0.3987.149 Safari/537.36'

    }

    allowed_domains = ["cruzverde.cl"]
    start_urls = ["https://www.cruzverde.cl/medicamentos/"]
    download_delay = 1

    rules = (
        Rule(
            LinkExtractor(
                allow=r'start=',
                tags=('a', 'button'),
                attrs=('href', 'data-url')
            ), follow=True, callback='parse_drugstore'
        ),
    )

    def parse_drugstore(self, response):
        sel = Selector(response)

        products = sel.xpath('//div[@class="col-12 col-lg-4"]')

        for product in products:
            item = ItemLoader(Drugstore(), product)

            item.add_xpath('name',
                           './/div[@class="tile-body px-3 pt-3 pb-0 d-flex flex-column pb-0"]//div[@class="pdp-link"]/a/text()', MapCompose(lambda i: i.replace('\n', '').replace('\r', '')))

            item.add_xpath('price',
                           './/span[contains(@class, "value")]/text()', MapCompose(lambda i: i.replace('\n', '').replace('\r', '').replace(' ', '')))

            yield item.load_item()

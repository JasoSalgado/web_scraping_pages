from scrapy.item import Field, Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import MapCompose


class Article(Item):
    """Data to extract"""
    title = Field()
    price = Field()
    description = Field()


class MercadoLibreCrawler(CrawlSpider):
    """App name"""
    name = 'mercadolibre'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
        'CLOSESPIDER_PAGECOUNT': 20
    }

    download_delay = 1

    # Domains to look for
    allowed_domains = ['listado.mercadolibre.com.mx', 'articulo.mercadolibre.com.mx']

    # Seed urls
    start_urls = ['https://listado.mercadolibre.com.mx/libros-programaci%C3%B3n#D[A:libros%20programaci%C3%B3n]']

    rules = (
        # Pagination
        Rule(
            LinkExtractor(
                allow=r'/_Desde_'
            ), follow=True
        ),
        # Product´s detail
        Rule(
            LinkExtractor(
                allow=r'/MLM-'
            ), follow=True, callback='parse_items'
        ),
    )

    def clean_text(self, text):
        cleaned_text = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
        return cleaned_text

    def parse_items(self, response):
        item = ItemLoader(Article(), response)
        item.add_xpath('title', '//h1/text()', MapCompose(self.clean_text))
        item.add_xpath('description', '//p[@class="ui-pdp-description__content"]/text()', MapCompose(self.clean_text))
        item.add_xpath('price', '//span[@class="price-tag-fraction"]/text()')

        yield item.load_item()
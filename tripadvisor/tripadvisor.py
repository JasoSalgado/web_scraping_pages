"""Scraping many pages"""
from scrapy.item import Field, Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader

# Defining our extraction
class Hotel(Item):
    name = Field()
    price = Field()
    description = Field()
    amenities = Field()


class TripAdvisor(CrawlSpider):
    """CrawlSpider allows to go vertical or horizontally in the page"""
    name = "Hotels"
    custom_settings = {
        "USER-AGENT": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36"
    }
    start_urls = ["https://www.tripadvisor.com/Hotels-g153445-Ixtapa_Zihuatanejo_de_Azueta_Pacific_Coast-Hotels.html"]

    # Not to be banned
    download_delay = 2

    # Follow these rules and if they are true, return data
    rules = (
        Rule(
            LinkExtractor(
                # It is just going to extract links with /Hotel_Review-
                allow=r'/Hotel_Review-'
            ), follow=True, callback="parse_hotel"
        ),
    )


    def remove_dollar_symbol(self, text):
        new_text = text.replace('MX$', '')
        new_text = new_text.replace('\n', '').replace('\r', '').replace('\t', '')
        return new_text


    # We are going to call parse_hotel when aforementioned conditions are true
    def parse_hotel(self, response):
        sel = Selector(response)
        item = ItemLoader(Hotel(), sel)

        item.add_xpath('name', '//h1[@id="HEADING"]/text()')
        item.add_xpath('price', '//div[@class="_36QMXqQj autoResize"]/text()',
                       MapCompose(self.remove_dollar_symbol))
        item.add_xpath('description', '//div[@class="cPQsENeY"]/text()')
        item.add_xpath('amenities', '//div[contains(@class, "_2rdvbNSg")]/text()')

        yield item.load_item()


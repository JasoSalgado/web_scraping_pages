from scrapy.item import Field, Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader

class Opinions(Item):
    title = Field()
    rating = Field()
    content = Field()
    author = Field()

class TripAdvisorCrawling(CrawlSpider):
    name = 'TripAdvisorOpinions'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
        'CLOSESPIDER_PAGECOUNT': 100
    }

    allowed_domains = ['tripadvisor.com']
    start_urls = ['https://www.tripadvisor.com/Hotels-g303845-Guayaquil_Guayas_Province-Hotels.html']

    download_delay = 1

    rules = (
        # Hotel´s pagination vertically
        Rule(  # https://www.tripadvisor.com/Hotels-g303845-Guayaquil_Guayas_Province-Hotels.html
            LinkExtractor(
                allow=r'-oa\d+-'
            ), follow=True),
        # Hotel´s detail
        Rule(
            LinkExtractor(
                allow=r'/Hotel_Review-',
                restrict_xpaths=['//div[@id="taplc_hsx_hotel_list_lite_dusty_hotels_combined_sponsored_0"]']
            ), follow=True),
        # Opinions vertically
        Rule(
            LinkExtractor(
                allow=r'-or\d+-'
            ), follow=True),
        # User´s profile detail
        Rule(
            LinkExtractor(
                allow=r'/Profile/',
                restrict_xpaths=['//div[@data-test-target="reviews-tab"]']
            ), follow=True, callback='parse_opinion'),
    # We use a callback because, we are going to extract the user´s opinions
    )

    # https://www.tripadvisor.com/Profile/daniaquir0la?fid=25838fc7-bedc-4d3b-b2bc-c0d5a72d6736
    def parse_opinion(self, response):
        sel = Selector(response)
        opinions = sel.xpath('//div[@id="content"]/div/div')
        author = sel.xpath('//h1/span/text()').get()
        for opinion in opinions:
            item = ItemLoader(Opinions(), opinion)
            item.add_value('author', author)
            item.add_xpath('title',
                           './/div[@class="social-section-review-ReviewSection__title--dTu08 social-section-review-ReviewSection__linked--kI3zg"]/text()')
            item.add_xpath('content', './/q/text()', MapCompose(lambda i: i.replace('\n', '').replace('\r', '')))
            item.add_xpath('rating',
                           './/div[contains(@class, "social-section-review")]//span[contains(@class, "ui_bubble_rating")]/@class',
                           MapCompose(lambda i: i.split('_')[-1]))
            yield item.load_item()
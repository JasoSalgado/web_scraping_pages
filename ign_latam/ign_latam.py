from scrapy.item import Field, Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader

class Article(Item):
    title = Field()
    content = Field()

class Review(Item):
    title = Field()
    rating = Field()

class Video(Item):
    title = Field()
    publishing_date = Field()


# We define our crawlspider
class IGNCrawler(CrawlSpider):
    name = 'ign'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
        'CLOSESPIDER_PAGECOUNT': 50
    }

    allowed_domains = ['latam.ign.com']
    start_urls = ['https://latam.ign.com/se/?model=article&q=ps4']
    download_delay = 1


    # Rules
    rules = (
        # Horizontality by type of information
        Rule(
            LinkExtractor(
                allow=r'type='
            ), follow=True
        ),
        # Horizontality by pagination
        Rule(
            LinkExtractor(
                allow=r'&page=\d+'
            ), follow=True
        ),
        # One rule by every type of content to go vertically
        # REVIEWS
        Rule(
            LinkExtractor(
                allow=r'/review/'
            ), follow=True, callback='parse_review'
        ),
        # ARTICLES
        Rule(
            LinkExtractor(
                allow=r'/news/'
            ), follow=True, callback='parse_news' # callback extracts info
        ),
        # VIDEOS
        Rule(
            LinkExtractor(
                allow=r'/video/'
            ), follow=True, callback='parse_video'
        ),
    )

    # We define our functions
    def parse_review(self, response):
        item = ItemLoader(Review(), response)

        item.add_xpath('title', '//h1/text()')
        item.add_xpath('rating', '//span[@class=""side-wrapper side-wrapper hexagon-content]/text()')
        yield item.load_item()


    def parse_video(self, response):
        item = ItemLoader(Video(), response)

        item.add_xpath('title', '//h1/text()')
        item.add_xpath('publishing_date', '//span[@class="publish-date"]/text()')
        yield item.load_item()


    def parse_news(self, response):
        item = ItemLoader(Article(), response)

        item.add_xpath('title', '//h1/text()')
        item.add_xpath('content', '//div[@id="id_text"]//*/text()')
        yield item.load_item()
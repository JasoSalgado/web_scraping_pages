from scrapy.item import Field, Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader

class Question(Item):
    """Extracting every question and description"""
    question = Field()
    description = Field()


# Core of scrapy
class StackoverflowSpider(Spider):
    """Extracting from a single page"""
    name = "MySpider"

    custom_settings = {
        "USER-AGENT": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36"
    }

    start_urls = ["https://www.stackoverflow.com/questions"]

    def parse(self, response):
        """Parsing the response to get the data"""
        select = Selector(response)
        questions = select.xpath('//div[@id="questions"]//div[@class="question-summary"]')
        for question in questions:
            # It receives an instance from Question() and the selector
            item = ItemLoader(Question(), question)
            # We add the information in the variable item
            # We charge the property question
            # And the second parameter is where the data we need is located
            item.add_xpath('question', './/h3/a/text()')
            # Now, we charge description data
            item.add_xpath('description', './/div[@class="excerpt"]/text()')

            # This sends the information to a file
            yield item.load_item()

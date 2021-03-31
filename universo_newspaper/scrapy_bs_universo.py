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

class UniversoSpider(Spider):
    name = 'UniversoSpyder'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36'
    }

    start_urls = ['https://www.eluniverso.com/deportes']

    def parse(self, response):
        soup = BeautifulSoup(response.body)
        news_container = soup.find_all('div', class_="view-content")
        id = 0

        for container in news_container:
            news = container.find_all('div', class_="posts", recursive=False)

            for n in news:
                item = ItemLoader(News(), response.body)
                title = n.find('h2').text
                description = n.find('p')

                if description:
                    item.add_value('description', description)
                else:
                    item.add_value('description', 'N/A')
                item.add_value('title', title)
                item.add_value('description', description)
                id += 1

                yield item.load_item()


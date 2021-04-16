from twisted.internet import reactor
from twisted.internet.task import LoopingCall
from scrapy.crawler import CrawlerRunner
from scrapy.spiders import Spider
from pymongo import MongoClient

client = MongoClient('localhost')
db = client['weather']
col = db['scrapy_weather']

class ExtractWeather(Spider):
    name = 'WeatherExtraction'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
        'CLOSESPIDER_PAGECOUNT': 20,
        'LOG_ENABLED': False
    }

    start_urls = [
        "https://www.accuweather.com/es/ec/guayaquil/127947/weather-forecast/127947",
        "https://www.accuweather.com/es/ec/quito/129846/weather-forecast/129846",
        "https://www.accuweather.com/es/es/madrid/308526/weather-forecast/308526"
    ]

    def parse(self, response):
        print(response)
        city = response.xpath('//h1/text()').get()
        current_weather = response.xpath('//a[contains(@class, "card current")]//div[@class="temp"]/span[1]/text()').get()
        real_feel = response.xpath('//a[contains(@class, "card current")]//div[@class="real-feel"]/text()').get()
        city = city.replace('\n', '').replace('\r', '').strip()
        current_weather = current_weather.replace('°', '').replace('\n', '').replace('\r', '').strip()
        real_feel = real_feel.replace('RealFeel®', '').replace('°', '').replace('\n', '').replace('\r', '').strip()

        col.update_one({
            'city': city
        }, {
            '$set': {
                'city': city,
                'current_weather': current_weather,
                'real_feel': real_feel
            }
        }, upsert=True)

# Logic to automate
runner = CrawlerRunner()
task = LoopingCall(lambda: runner.crawl(ExtractWeather))
task.start(20)
reactor.run()
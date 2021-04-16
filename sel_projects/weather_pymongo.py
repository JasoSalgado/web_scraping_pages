"""
Update data to MongoDB from Selenium
"""

# Modules
import schedule
import time
from selenium import webdriver
from pymongo import MongoClient

# Instance MongoDB
client = MongoClient('localhost')
db = client['weather']
col = db['weather']

# Seed urls
start_urls = [
    "https://www.accuweather.com/es/ec/guayaquil/127947/weather-forecast/127947",
    "https://www.accuweather.com/es/ec/quito/129846/weather-forecast/129846",
    "https://www.accuweather.com/es/es/madrid/308526/weather-forecast/308526"
]

def extract_data():
    driver = webdriver.Chrome('./chromedriver.exe')

    for url in start_urls:
        driver.get(url)

        city = driver.find_element_by_xpath('//h1').text
        current_weather = driver.find_element_by_xpath('//a[contains(@class, "card current")]//div[@class="temp"]/span[1]').text
        real_feel = driver.find_element_by_xpath('//a[contains(@class, "card current")]//div[@class="real-feel"]').text

        city = city.replace('\n', '').replace('\r', '').strip()
        current_weather = current_weather.replace('°', '').replace('\n', '').replace('\r', '').strip()
        real_feel = real_feel.replace('RealFeel®', '').replace('°', '').replace('\n', '').replace('\r', '').strip()

        # This is a unique property.
        col.update_one({
            'city': city
        }, {
            '$set': {
                'city': city,
                'current_weather': current_weather,
                'real_feel': real_feel
            }
        }, upsert=True)

        print(city)
        print(current_weather)
        print(real_feel)
        print()
    driver.close()

# Extract automatically
schedule.every(5).minutes.do(extract_data())

while True:
    schedule.run_pending()
    time.sleep(1)
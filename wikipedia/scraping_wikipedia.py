# Modules
import requests
from lxml import html

# Headers. We have to change the user-agent not to be detected as a robot
headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36"
}

url = "https://www.wikipedia.org/"
response = requests.get(url, headers=headers)

# Using library lxml to create a parser
parser = html.fromstring(response.text)

# english = parser.get_element_by_id("js-link-box-en")
# print(english.text_content())

# Using xpath
# languages = parser.xpath("//div[contains(@class, 'central-featured-lang')]//strong/text()")
# for language in languages:
#     print(language)

languages = parser.find_class('central-featured-lang')
for language in languages:
    print(language.text_content())

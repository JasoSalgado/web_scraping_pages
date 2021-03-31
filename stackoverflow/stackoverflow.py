import requests
from bs4 import BeautifulSoup

# Headers. We have to change the user-agent not to be detected as a robot
headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36"
}

url = "https://stackoverflow.com/questions"

response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text)

questions_container = soup.find(id='questions')
# Look for in the questions_container because, soup has all the html tree
questions_list = questions_container.find_all('div', class_="question-summary")

for question in questions_list:
    question_element_text = question.find('h3')
    question_text = question_element_text.text
    question_description = question_element_text.find_next_sibling('div').text

    # Removing strange characters from data
    question_description = question_description.replace('\n', '').replace('\r', '').strip()
    print(question_text)
    print(question_description)
    print()

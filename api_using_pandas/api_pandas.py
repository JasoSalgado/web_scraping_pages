"""
Extract name, reviews and ratings from Python courses
Save them in a CSV
"""

# Modules
import requests
import pandas as pd
import json

headers = {
    "referer": "https://www.udemy.com/courses/search/?src=ukw&q=python",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36",
}

# This list is helping me to iterate the parameter API page
total_courses = []
for i in range(1, 4):
    url_api = 'https://www.udemy.com/api-2.0/search-courses/?fields[locale]=simple_english_title&src=ukw&q=python&p=' + str(i)

    response = requests.get(url_api, headers=headers)

    # This is a json response but, requests automatically converts it in a Python dictionary
    data = response.json()

    # Extract data from dictionary
    courses = data['courses']
    for course in courses:
        total_courses.append({
            "title": course["title"],
            "num_reviews": course["num_reviews"],
            "rating": course["rating"]
        })

df = pd.DataFrame(total_courses)
print(df)

df.to_csv("udemy_courses.csv")
import csv

import requests
from bs4 import BeautifulSoup


def get_description_rating_from_html(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    data = soup.find(attrs={"data-purpose": "safely-set-inner-html:description:description"})
    if data is None:
        return None, None
    rating = soup.find(attrs={"data-purpose": "rating-number"})
    return data.text, rating.text


def get_description_from_html(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    data = soup.find(class_="description")
    if data is None:
        return None
    return data.text


def get_all_udemy_data():
    with open('udemy_courses.csv', newline='', encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)

        with open('new_names.csv', 'w', encoding='utf-8') as new_csv_file:
            fieldnames = ['index', 'name', 'url', 'rating', 'difficulty', 'tags', 'website', 'description']

            csv_writer = csv.writer(new_csv_file)
            csv_writer.writerow(fieldnames)

            i = 0
            for row in csv_reader:
                description, rating = get_description_rating_from_html(row['url'])
                if description is not None:
                    csv_writer.writerow(
                        [i, row['course_title'], row['url'], rating, row['level'], row['subject'], "Udemy",
                         description])
                    i = i + 1


def get_all_coursera_data():
    with open('coursera-course-detail-data.csv', newline='', encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)

        with open('edited_info2_coursera.csv', 'w', encoding='utf-8') as new_csv_file:
            fieldnames = ['index', 'name', 'url', 'rating', 'difficulty', 'tags', 'website', 'description']

            csv_writer = csv.writer(new_csv_file)
            csv_writer.writerow(fieldnames)

            i = 0
            for row in csv_reader:
                description = get_description_from_html(row['Url'])
                if description is not None:
                    csv_writer.writerow(
                        [i, row['Name'], row['Url'], row['Rating'], row['Difficulty'], row['Tags'], "Coursera",
                         description])
                    i = i + 1


def get_description_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    data = soup.find(class_="description")
    # data = soup.find('div', class_='content-inner')
    print(data.text)


if __name__ == '__main__':
    # get_all_udemy_data()
    get_all_coursera_data()
    # get_description_from_url('https://www.coursera.org/learn/taknulujia-alnnanu2')

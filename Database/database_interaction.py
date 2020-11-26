import csv
import mysql.connector
from decimal import Decimal


def create_recommendation_database():
    db = mysql.connector.connect(host='localhost', user='root', passwd='admin')
    mycursor = db.cursor()
    mycursor.execute("CREATE DATABASE recommendation")
    # mycursor.execute("SHOW DATABASES")
    # for d in mycursor:
    #     print(d)
    db.close()


def create_courses_table():
    db = mysql.connector.connect(host='localhost', user='root', passwd='admin', database='recommendation')
    mycursor = db.cursor()
    mycursor.execute(
        "CREATE TABLE courses(id INT AUTO_INCREMENT PRIMARY KEY, name MEDIUMTEXT, url MEDIUMTEXT, rating DOUBLE, difficulty TEXT, tags TEXT,website MEDIUMTEXT, description LONGTEXT)")
    # mycursor.execute("SHOW TABLES")
    # for tb in mycursor:
    #     print(tb)
    db.close()


def insert_courses_udemy_into_table():
    mydb = mysql.connector.connect(host='localhost', user='root', passwd='admin', db='recommendation', use_unicode=True,
                                   charset='utf8')
    cursor = mydb.cursor()
    with open('../DataSetManipulation/edited_info_udemy.csv',  newline='', encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            try:
                cursor.execute(
                    'INSERT INTO courses(name, url, rating, difficulty, tags, website, description) VALUES("%s", "%s", "%s", "%s", "%s", "%s", "%s")',
                [row['name'], row['url'], float(row['rating']), row['difficulty'], row['tags'], row['website'], row['description']])
            except Exception as e:
                print(e)
                print(row)
                break
    mydb.commit()
    cursor.close()


def insert_courses_coursera_into_table():
    mydb = mysql.connector.connect(host='localhost', user='root', passwd='admin', db='recommendation', use_unicode=True,
                                   charset='utf8')
    cursor = mydb.cursor()
    with open('../DataSetManipulation/edited_info2_coursera.csv',  newline='', encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            try:
                cursor.execute(
                    'INSERT INTO courses(name, url, rating, difficulty, tags, website, description) VALUES("%s", "%s", "%s", "%s", "%s", "%s", "%s")',
                [row['name'], row['url'], float(row['rating']), row['difficulty'], row['tags'][1:-1], row['website'], row['description']])
            except Exception as e:
                print(e)
                print(row)
                break
    mydb.commit()
    cursor.close()


# de inlocuit preluarea descrierea din fisier cu preluarea de db
def get_all_descriptions():
    with open('../DataSetManipulation/edited_info2_coursera.csv', newline='', encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)

        course_desc = {}
        for row in csv_reader:
            course_desc[row['index']] = row['description']
        return course_desc


def get_all_courses():
    return 'All courses'


def get_course_by_id(id):
    return 'This is book with the id'


if __name__ == '__main__':
    # insert_courses_udemy_into_table()
    insert_courses_coursera_into_table()

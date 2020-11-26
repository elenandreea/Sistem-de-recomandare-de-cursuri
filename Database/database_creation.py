import csv
import mysql.connector


def create_recommendation_database():
    db = mysql.connector.connect(host='localhost', user='root', passwd='admin')
    mycursor = db.cursor()
    mycursor.execute("CREATE DATABASE recommendation")
    db.close()


def create_courses_table():
    db = mysql.connector.connect(host='localhost', user='root', passwd='admin', database='recommendation')
    mycursor = db.cursor()
    mycursor.execute(
        "CREATE TABLE courses(id INT AUTO_INCREMENT PRIMARY KEY, name MEDIUMTEXT, url MEDIUMTEXT, rating DOUBLE, difficulty TEXT, tags TEXT,website MEDIUMTEXT, description LONGTEXT)")
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


if __name__ == '__main__':
    # insert_courses_udemy_into_table()
    insert_courses_coursera_into_table()
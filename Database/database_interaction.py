import csv
import mysql.connector


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


# if __name__ == '__main__':
    # insert_courses_udemy_into_table()
    # insert_courses_coursera_into_table()

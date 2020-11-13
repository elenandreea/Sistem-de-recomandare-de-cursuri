import csv


#de inlocuit preluarea descrierea din fisier cu preluarea de db
def get_all_descriptions():
    with open('../DataSetManipulation/edited_info2_coursera.csv', newline='', encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)

        course_desc = {}
        for row in csv_reader:
            course_desc[row['index']] = row['description']
        return course_desc

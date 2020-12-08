import csv
import mysql.connector


def get_id_and_url():
    mydb = mysql.connector.connect(host='localhost', user='root', passwd='admin', db='recommendation', use_unicode=True,
                                   charset='utf8')
    cursor = mydb.cursor()

    query = "SELECT id, url FROM courses WHERE website LIKE '%Coursera%'"
    try:
        cursor.execute(query)
    except Exception as e:
        print(e)

    data = cursor.fetchall()
    cursor.close()

    result = {}
    for d in data:
        key = d[1][1:-1].split("https://coursera.org/learn/")[1]
        result[key] = d[0]

    return result


# rating, user, idcurs
def create_reviews_table():
    db = mysql.connector.connect(host='localhost', user='root', passwd='admin', database='recommendation')
    mycursor = db.cursor()
    mycursor.execute("CREATE TABLE reviews(id_curs INT NOT NULL, user TEXT, rating DOUBLE)")
    db.close()


def get_users_review():

    rows_db = get_id_and_url()
    keys_db = rows_db.keys()

    with open('../Datasets/Coursera_reviews.csv', newline='', encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)

        result = {}
        for row_csv in csv_reader:
            if row_csv['course_id'] in keys_db:
                reviewer = row_csv['reviewers'][3:]
                course_id = rows_db[row_csv['course_id']]
                if (reviewer, row_csv['course_id']) not in result.keys():
                    result[(reviewer, course_id)] = float(row_csv['rating'])
        return result


def write_users_review_to_csv():
    result = get_users_review()
    print(len(result))

    with open('../Datasets/new_users_review.csv', 'w', encoding='utf-8') as new_csv_file:
        fieldnames = ['course_id', 'reviewer', 'rating']

        csv_writer = csv.writer(new_csv_file)
        csv_writer.writerow(fieldnames)

        for reviewer, course_id in result:
            csv_writer.writerow([reviewer, course_id, result[reviewer, course_id]])


def insert_into_users_table():
    mydb = mysql.connector.connect(host='localhost', user='root', passwd='admin', db='recommendation', use_unicode=True,
                                   charset='utf8')
    cursor = mydb.cursor()
    result = get_users_review()

    for reviewer, course_id in result:
        try:
            cursor.execute('INSERT INTO reviews(id_curs, user, rating) VALUES("%s", "%s", "%s")',
                           [course_id, reviewer, result[reviewer, course_id]])
        except Exception as e:
            print(e)
            print(reviewer, course_id)
            break
    mydb.commit()
    cursor.close()


if __name__ == '__main__':
    # create_reviews_table()
    # write_users_review_to_csv()
    insert_into_users_table()

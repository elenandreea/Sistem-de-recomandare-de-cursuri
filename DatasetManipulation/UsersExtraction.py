import csv
import mysql.connector
import re


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


def get_id_for_user(user_name):
    mydb = mysql.connector.connect(host='localhost', user='root', passwd='admin', db='recommendation', use_unicode=True,
                                   charset='utf8')
    cursor = mydb.cursor(buffered=True)
    sql_select_query = "select id_user from users where name_user = %s"

    try:
        cursor.execute(sql_select_query, (user_name,))
    except Exception as e:
        print(e)
        return None

    data = cursor.fetchall()
    cursor.close()
    if not data:
        return None
    return data[0][0]


# id_curs, id_user, rating
def create_reviews_table():
    db = mysql.connector.connect(host='localhost', user='root', passwd='admin', database='recommendation')
    mycursor = db.cursor()
    mycursor.execute("CREATE TABLE reviews(id_user INT NOT NULL, id_curs INT NOT NULL, rating DOUBLE)")
    db.close()


def create_users_table():
    db = mysql.connector.connect(host='localhost', user='root', passwd='admin', database='recommendation')
    mycursor = db.cursor()
    mycursor.execute("CREATE TABLE users(id_user INT NOT NULL, name_user TEXT)")
    db.close()


def generate_IDs_for_users():
    with open('../Datasets/unique_users.csv', newline='', encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)

        with open('../Datasets/coursera_users.csv', 'w', encoding='utf-8') as new_csv_file:
            fieldnames = ['index', 'name']

            csv_writer = csv.writer(new_csv_file)
            csv_writer.writerow(fieldnames)

            i = 0
            for row in csv_reader:
                name = row['reviewers'][3:]
                regex = re.compile('[A-Z][a-z]*[ ][A-Z]')
                match = regex.match(str(name))
                if not bool(match):
                    continue
                csv_writer.writerow(
                    [i, name])
                i = i + 1
            print(i)


def insert_into_users_table():
    mydb = mysql.connector.connect(host='localhost', user='root', passwd='admin', db='recommendation', use_unicode=True,
                                   charset='utf8')
    cursor = mydb.cursor()

    with open('../Datasets/coursera_users.csv', newline='', encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row_csv in csv_reader:
            id_user = row_csv['index']
            name_user = row_csv['name']
            print(id_user, name_user)
            try:
                cursor.execute('INSERT INTO users(id_user, name_user) VALUES("%s", "%s")',
                           [int(id_user), name_user])
            except Exception as e:
                print(e)
                print(id_user, name_user)
                break
    mydb.commit()
    cursor.close()


def get_users_rating():
    rows_db = get_id_and_url()
    keys_db = rows_db.keys()
    course_count = {}

    with open('../Datasets/Coursera_reviews_unique.csv', newline='', encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)

        with open('../Datasets/user-course-rating.csv', 'w', encoding='utf-8') as new_csv_file:
            fieldnames = ['user_id', 'course_id', 'rating']

            csv_writer = csv.writer(new_csv_file)
            csv_writer.writerow(fieldnames)

            result = {}
            for row_csv in csv_reader:
                if row_csv['course_id'] in keys_db:
                    course_id = rows_db[row_csv['course_id']]
                    if course_id not in course_count:
                        course_count[course_id] = 1
                    else:
                        course_count[course_id] += 1
                        if course_count[course_id] > 100:
                            continue
                    reviewer = row_csv['reviewers'][3:]
                    reviewer_id = get_id_for_user("'" + reviewer + "'")
                    if reviewer_id is None:
                        continue
                    if (reviewer_id, row_csv['course_id']) not in result.keys():
                        result[(reviewer_id, course_id)] = float(row_csv['rating'])
                        csv_writer.writerow([reviewer_id, course_id, result[reviewer_id, course_id]])
                        print(reviewer_id, course_id)
    return result


def get_users_rating_review():
    rows_db = get_id_and_url()
    keys_db = rows_db.keys()
    course_count = {}

    with open('../Datasets/Coursera_reviews_unique.csv', newline='', encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)

        with open('../Datasets/user-course-rating-review.csv', 'w', encoding='utf-8') as new_csv_file:
            fieldnames = ['user_id', 'course_id', 'rating', 'reviews']

            csv_writer = csv.writer(new_csv_file)
            csv_writer.writerow(fieldnames)

            result = {}
            for row_csv in csv_reader:
                if row_csv['course_id'] in keys_db:
                    course_id = rows_db[row_csv['course_id']]
                    if course_id not in course_count:
                        course_count[course_id] = 1
                    else:
                        course_count[course_id] += 1
                        if course_count[course_id] > 100:
                            continue
                    reviewer = row_csv['reviewers'][3:]
                    reviewer_id = get_id_for_user("'" + reviewer + "'")
                    if reviewer_id is None:
                        continue
                    if (reviewer_id, row_csv['course_id']) not in result.keys():
                        reviews = row_csv['reviews']
                        result[(reviewer_id, course_id)] = float(row_csv['rating'])
                        csv_writer.writerow([reviewer_id, course_id, result[reviewer_id, course_id], reviews])
                        print(reviewer_id, course_id)
    return result


def write_users_review_to_csv():
    result = get_users_rating()
    print(len(result))

    with open('../Datasets/user-course-rating.csv', 'w', encoding='utf-8') as new_csv_file:
        fieldnames = ['user_id', 'course_id', 'rating']

        csv_writer = csv.writer(new_csv_file)
        csv_writer.writerow(fieldnames)

        for user_id, course_id in result:
            if user_id is not None:
                csv_writer.writerow([user_id, course_id, result[user_id, course_id]])


def id_course_csv():
    mydb = mysql.connector.connect(host='localhost', user='root', passwd='admin', db='recommendation', use_unicode=True,
                                   charset='utf8')
    cursor = mydb.cursor()
    with open('../Datasets/user-course-rating.csv',  newline='', encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)

        with open('../Datasets/id_courses_coursera.csv', 'w', encoding='utf-8') as new_csv_file:
            fieldnames = ['course_id', 'course_name']

            csv_writer = csv.writer(new_csv_file)
            csv_writer.writerow(fieldnames)

            courses = {}

            for row in csv_reader:
                course_id = row['course_id']
                if course_id in courses.keys():
                    continue
                print("course_id: ", course_id)
                try:
                    cursor.execute('SELECT name FROM courses WHERE id LIKE %s', [int(course_id)])
                    data = cursor.fetchall()
                    course_name = data[0][0]
                    print("course_name: ", course_name)
                    courses[course_id] = course_name
                except Exception as e:
                    print(e)
                    print(course_id, course_name)
                    break
                csv_writer.writerow(
                    [course_id, course_name])

        mydb.commit()
        cursor.close()


def insert_into_reviews_table():
    mydb = mysql.connector.connect(host='localhost', user='root', passwd='admin', db='recommendation', use_unicode=True,
                                   charset='utf8')
    cursor = mydb.cursor()
    result = get_users_rating()

    print("BEGIN INSERT")

    for user_id, course_id in result:
        try:
            cursor.execute('INSERT INTO reviews(id_user, id_curs, rating) VALUES("%s", "%s", "%s")',
                           [user_id, course_id, result[user_id, course_id]])
        except Exception as e:
            print(e)
            print(user_id, course_id)
            break
    mydb.commit()
    cursor.close()


if __name__ == '__main__':
    # create_reviews_table()
    # write_users_review_to_csv()
    # insert_into_users_table()
    # generate_IDs_for_users()
    # create_users_table()
    # insert_into_users_table()
    # create_reviews_table()
    # write_users_review_to_csv()
    # result = get_id_for_user("'Robert S'")
    print("HELLO")
    # get_users_review()
    # insert_into_reviews_table()
    # get_users_review()
    # id_course_csv()
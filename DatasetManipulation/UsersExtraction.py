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
        value = d[1][1:-1]
        result[d[0]] = value.split("https://coursera.org/learn/")[1]

    return result


# rating, user, idcurs
def create_reviews_table():
    db = mysql.connector.connect(host='localhost', user='root', passwd='admin', database='recommendation')
    mycursor = db.cursor()
    mycursor.execute(
        "CREATE TABLE reviews(id_curs INT NOT NULL, user MEDIUMTEXT, rating DOUBLE)")
    db.close()


#NOT DONE
def get_users_review():
    with open('../Datasets/Coursera_reviews.csv', newline='', encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)

        result = {}
        return result


#NOT DONE
def insert_into_users_table():
    mydb = mysql.connector.connect(host='localhost', user='root', passwd='admin', db='recommendation', use_unicode=True,
                                   charset='utf8')
    cursor = mydb.cursor()
    result = get_users_review()

    for row in result:
        try:
            cursor.execute('INSERT INTO reviews(id_curs, user, rating) VALUES("%s", "%s", "%s")',
                           [row['id_curs'], row['user'], float(row['rating'])])
        except Exception as e:
            print(e)
            print(row)
            break
    mydb.commit()
    cursor.close()


if __name__ == '__main__':
    create_reviews_table()
    # print(get_id_and_url())

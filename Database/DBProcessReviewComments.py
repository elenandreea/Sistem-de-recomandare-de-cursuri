import mysql.connector


def create_review_embeddings_table():
    db = mysql.connector.connect(host='localhost', user='root', passwd='admin', database='recommendation')
    cursor = db.cursor()
    cursor.execute("CREATE TABLE review_embeddings(id INT NOT NULL PRIMARY KEY, embed LONGTEXT)")
    db.close()


def delete_data_review_embeddings_table():
    db = mysql.connector.connect(host='localhost', user='root', passwd='admin', database='recommendation')
    cursor = db.cursor()
    cursor.execute("DELETE FROM recommendation.review_embeddings")
    db.close()


def insert_row_into_review_embeddings_table(row_id, row_comment):
    mydb = mysql.connector.connect(host='localhost', user='root', passwd='admin', db='recommendation', use_unicode=True,
                                   charset='utf8')
    cursor = mydb.cursor()

    try:
        cursor.execute('INSERT INTO review_embeddings(id, embed) VALUES("%s", "%s")', [row_id, row_comment])
    except Exception as e:
        print(e)
        print(row_id)

    mydb.commit()
    cursor.close()


def get_all_review_embeddings():
    mydb = mysql.connector.connect(host='localhost', user='root', passwd='admin', db='recommendation', use_unicode=True,
                                   charset='utf8')
    cursor = mydb.cursor()

    query = 'SELECT id, embed FROM review_embeddings'
    try:
        cursor.execute(query)
    except Exception as e:
        print(e)

    data = cursor.fetchall()
    cursor.close()

    result = {}
    for d in data:
        result[d[0]] = d[1][1:-1]

    return result


if __name__ == '__main__':
    create_review_embeddings_table()


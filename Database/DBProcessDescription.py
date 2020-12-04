import mysql.connector


def create_embeddings_table():
    db = mysql.connector.connect(host='localhost', user='root', passwd='admin', database='recommendation')
    cursor = db.cursor()
    cursor.execute("CREATE TABLE embeddings(id INT NOT NULL PRIMARY KEY, embed LONGTEXT)")
    db.close()


def insert_row_into_embeddings_table(row_id, row_desc):
    mydb = mysql.connector.connect(host='localhost', user='root', passwd='admin', db='recommendation', use_unicode=True,
                                   charset='utf8')
    cursor = mydb.cursor()

    try:
        cursor.execute('INSERT INTO embeddings(id, embed) VALUES("%s", "%s")', [row_id, row_desc])
    except Exception as e:
        print(e)
        print(row_id)

    mydb.commit()
    cursor.close()


def get_all_embeddings():
    mydb = mysql.connector.connect(host='localhost', user='root', passwd='admin', db='recommendation', use_unicode=True,
                                   charset='utf8')
    cursor = mydb.cursor()

    query = 'SELECT id, embed FROM embeddings'
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

# if __name__ == '__main__':
#     create_embeddings_table()

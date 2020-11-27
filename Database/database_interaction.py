import mysql.connector


def get_all_courses():
    mydb = mysql.connector.connect(host='localhost', user='root', passwd='admin', db='recommendation', use_unicode=True, charset='utf8')
    cursor = mydb.cursor()

    query = 'SELECT id, name, rating, website FROM courses'
    try:
        cursor.execute(query)
    except Exception as e:
        print(e)

    header = [x[0] for x in cursor.description]
    data = cursor.fetchall()
    cursor.close()

    result = []
    for d in data:
        name = d[1][1:-1]
        website = d[3][1:-1]
        result.append(dict(zip(header, (d[0], name, d[2], website))))

    return result


def get_course_by_id(id_course):
    mydb = mysql.connector.connect(host='localhost', user='root', passwd='admin', db='recommendation', use_unicode=True, charset='utf8')
    cursor = mydb.cursor()

    query = 'SELECT * FROM courses where id = ' + str(id_course)
    try:
        cursor.execute(query)
    except Exception as e:
        print(e)

    header = [x[0] for x in cursor.description]
    data = cursor.fetchone()
    cursor.close()

    data = [d[1:-1] if not isinstance(d, (int, float)) else d for d in data]
    result = dict(zip(header, data))

    return result


def get_all_descriptions():
    mydb = mysql.connector.connect(host='localhost', user='root', passwd='admin', db='recommendation', use_unicode=True, charset='utf8')
    cursor = mydb.cursor()

    query = 'SELECT id, description FROM courses'
    try:
        cursor.execute(query)
    except Exception as e:
        print(e)

    data = cursor.fetchall()
    cursor.close()

    result = list((d[0], d[1][1:-1]) for d in data)

    return result


def get_courses_by_ids(ids):
    mydb = mysql.connector.connect(host='localhost', user='root', passwd='admin', db='recommendation', use_unicode=True, charset='utf8')
    cursor = mydb.cursor()

    data = []
    header = [x[0] for x in cursor.description]
    for course_id in ids:
        query = 'SELECT id, name, rating, website FROM courses where id = ' + str(course_id)
        try:
            cursor.execute(query)
        except Exception as e:
            print(e)

        data += [cursor.fetchone()]

    cursor.close()

    result = []
    for d in data:
        name = d[1][1:-1]
        website = d[3][1:-1]
        result.append(dict(zip(header, (d[0], name, d[2], website))))

    return result

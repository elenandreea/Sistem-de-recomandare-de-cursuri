import mysql.connector
import time


def get_all_courses():
    mydb = mysql.connector.connect(host='localhost', user='root', passwd='admin', db='recommendation', use_unicode=True,
                                   charset='utf8')
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


def get_top_100_courses_with_all_details():
    mydb = mysql.connector.connect(host='localhost', user='root', passwd='admin', db='recommendation', use_unicode=True,
                                   charset='utf8')
    cursor = mydb.cursor()

    query = 'SELECT id, name, url, rating, difficulty, tags, website, description FROM courses ORDER BY rating desc LIMIT 200 '
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
        url = d[2][1:-1]
        difficulty = d[4][1:-1]
        tags = d[5][1:-1]
        website = d[6][1:-1]
        description = d[7][1:-1]
        result.append(dict(zip(header, (d[0], name, url, d[3], difficulty, tags, website, description))))

    return result


def get_course_by_id(id_course):
    mydb = mysql.connector.connect(host='localhost', user='root', passwd='admin', db='recommendation', use_unicode=True,
                                   charset='utf8')
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
    mydb = mysql.connector.connect(host='localhost', user='root', passwd='admin', db='recommendation', use_unicode=True,
                                   charset='utf8')
    cursor = mydb.cursor()

    query = 'SELECT id, description FROM courses'
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


def get_courses_by_ids(ids):
    mydb = mysql.connector.connect(host='localhost', user='root', passwd='admin', db='recommendation', use_unicode=True,
                                   charset='utf8')
    cursor = mydb.cursor()
    start_time = time.time()
    format_strings = ','.join(['%s'] * len(ids))
    try:
        cursor.execute("SELECT id, name, rating, website FROM courses where id IN (%s)" % format_strings, tuple(ids))
    except Exception as e:
        print(e)

    header = [x[0] for x in cursor.description]
    data = cursor.fetchall()

    print(time.time() - start_time)
    cursor.close()

    result = []
    for d in data:
        name = d[1][1:-1]
        website = d[3][1:-1]
        result.append(dict(zip(header, (d[0], name, d[2], website))))

    return result


def get_courses_by_ids_ms(ids):
    mydb = mysql.connector.connect(host='localhost', user='root', passwd='admin', db='recommendation', use_unicode=True,
                                   charset='utf8')
    cursor = mydb.cursor()

    header = []
    data = []
    start_time = time.time()
    for course_id in ids:
        query = 'SELECT id, name, rating, website FROM courses where id = ' + str(course_id)
        try:
            cursor.execute(query)
        except Exception as e:
            print(e)

        header = [x[0] for x in cursor.description]
        data += [cursor.fetchone()]

    print(time.time() - start_time)
    cursor.close()

    result = []
    for d in data:
        name = d[1][1:-1]
        website = d[3][1:-1]
        result.append(dict(zip(header, (d[0], name, d[2], website))))

    return result

def get_courses_with_filters(filters):
    mydb = mysql.connector.connect(host='localhost', user='root', passwd='admin', db='recommendation', use_unicode=True,
                                   charset='utf8')
    cursor = mydb.cursor()

    query_where = 'WHERE 1'

    for filter in filters:
        filter = list(filter.items())

        for (key, value) in filter:
            if key == 'search' and value[0] != None:
                query_where += ' AND name LIKE "%' + value[0] + '%"'
            elif key == "rating" and value != []:
                query_where += " AND rating > " + value[0]
            elif value != []:
                query_where += " AND (" + key + " = 1"
                for val in value:
                    query_where += " OR " + key + ' LIKE "%' + val + '%"'
                query_where += ")"

    query = 'SELECT id, name, url, rating, difficulty, tags, website, description FROM courses ' +query_where+ ' ORDER BY rating desc LIMIT 200 '
    print(query)
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
        url = d[2][1:-1]
        difficulty = d[4][1:-1]
        tags = d[5][1:-1]
        website = d[6][1:-1]
        description = d[7][1:-1]
        result.append(dict(zip(header, (d[0], name, url, d[3], difficulty, tags, website, description))))

    return result
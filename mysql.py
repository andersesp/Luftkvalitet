import pymysql.cursors

connection = pymysql.connect(host='localhost',
                            user = 'python',
                            password = 'raspberry',
                            db = 'timesverdier',
                            charset='utf8mb4',
                            cursorclass = pymysql.cursors.DictCursor)
try:
    with connection.cursor() as cursor:
        # Create a new record
        sql = "INSERT INTO `kirkeveien_tbl` (`timestamp`, `CO`) VALUES (%s, %s)"
        cursor.execute(sql, ('1000-01-01 00:00:00', '10.4'))

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()

    #with connection.cursor() as cursor:
        # Read a single record
        #sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
        #cursor.execute(sql, ('webmaster@python.org',))
        #result = cursor.fetchone()
        #print(result)
finally:
    connection.close()

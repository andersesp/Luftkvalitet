 # -- coding: utf-8 -- 
import time
import datetime
import pymysql.cursors



tiden = datetime.date.today()

tiden = tiden.strftime('%Y-%m-%d')
print tiden
#streng = "Jeg lever @AndersEspeseth " + tiden

time = "12:00:00"
komp = ["airqnow", "airq24"]
values = ["asf", "asdfas"]

connection = pymysql.connect(host='localhost',
                             user = 'python',
                             password = 'raspberry',
                             db = 'test',
                             charset='utf8mb4',
                             cursorclass = pymysql.cursors.DictCursor,
                             autocommit = True)
with connection.cursor() as cursor:

    sql1 = "INSERT INTO %s (`ttime`" %('testdata')
    sql2 = "VALUES ('%s'" %time
    
    for i in range(0, len(komp),1):
        sql1 +=",`" + komp[i] + "`"
        sql2 +=",'" + values[i] + "'"
    sql1 += ") "
    sql2 += ")"
    sql = sql1 + sql2
#sql = "INSERT INTO %s (`ttime`) VALUES ('%s')" %('testdata', time)
    print sql
    cursor.execute(sql)

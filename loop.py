 # -- coding: utf-8 -- 
from mysql2 import fetchAndFillMySQLData
import schedule
import time


fetchAndFillMySQLData()
schedule.every(60).minutes.do(fetchAndFillMySQLData)

while 1:
    schedule.run_pending()
    time.sleep(1)


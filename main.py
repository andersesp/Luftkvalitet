 # -- coding: utf-8 -- 
from mysql2 import fetchAndFillMySQLData
import schedule
import time
import logging

logging.basicConfig(filename='myapp.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
logging.getLogger("urllib3").setLevel(logging.WARNING)          # Unngår debug og info fra requests-biblioteket
logging.debug("Running main function")
fetchAndFillMySQLData()
schedule.every(60).minutes.do(fetchAndFillMySQLData)

while 1:
    schedule.run_pending()
    time.sleep(1)


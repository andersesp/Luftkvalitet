 # -- coding: utf-8 -- 
from mysql2 import fetchAndFillMySQLData
import schedule
import time
import logging


def main():
    logging.basicConfig(filename='myapp.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
    logging.getLogger("urllib3").setLevel(logging.WARNING)          # Unngår debug og info fra requests-biblioteket
    logging.debug("Running main function")
    fetchAndFillMySQLData()
    schedule.every(30).minutes.do(fetchAndFillMySQLData)

    while 1:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except Exception, e:
         logging.error("main crashed {0}".format(str(e)))

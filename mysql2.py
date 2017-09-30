# -- coding: utf-8 --

from lxml import html                                           # Brukes for å kunne hente data fra nett
import requests                                                 # Brukes for å kunne hente data fra nett
import pymysql.cursors                                          # Brukes for å skrive til MySQL-database
import schedule                                                 # Brukes for å schedule funksjoner
import time
import datetime
import logging
from setup import setupStations, getConnection

# Tar inn timestamp på formatet "HH:mm:ss", og legger til en time til timestampen. Dette gjøres fordi luftkvalitet.info alltid viser timestamps i vintertid
# Det bør fikses slik at det ikke legges til en time dersom det faktisk er vintertid.
def correctTimestamp(timestamp):
    hour = timestamp[0] + timestamp[1]
    if hour == "23":
        hour = 0
    else:
        hour = int(hour) + 1

    hour = str(hour)
    newtimestamp = ""
    if len(hour) == 1:
        newtimestamp += "0"
        newtimestamp += hour
    else:
        newtimestamp += hour[0]
        newtimestamp += hour[1]

    for i in range(2, len(timestamp),1):
        newtimestamp += timestamp[i]

    logging.debug(newtimestamp)
    return  newtimestamp





def fetchAndFillMySQLData():
    print "From FetchAndFillMySQLData" + str(datetime.datetime.now())
    # Fyller inn URL, antall målinger og tabellnavn per stasjon
    stationInfo = setupStations()


    #Kobler til mysql database
    try:
        connection = getConnection()
    except:
        print "Failed to connect to MySQL-server"

    #Går igjennom for hver stasjon
    for x in range(0,len(stationInfo),1):
        #Henter dagens dato
        tiden = datetime.date.today()
        tiden = tiden.strftime('%Y-%m-%d')
        
        #Henter måledata
        page = requests.get(stationInfo[x].url)
        tree = html.fromstring(page.content)
        
        #Henter stasjonsnavn, unødvendig? Kun Debug?
        stationNameXpath = '//span[@id="ctl00_cph_Text_ctl00_lTitle"]/text()'
        stationName = tree.xpath(stationNameXpath)[0].encode('iso-8859-1')
        logging.debug(stationName)
        
        #Setter opp tabeller for data, gjøres for hver stasjon pga forskjellige målinger
        komponent = [None for _ in range(stationInfo[x].nmrOfMeasurements)]
        verdi = [None for _ in range(stationInfo[x].nmrOfMeasurements)]
        
        # Går igjennom nettsiden og henter ut verdier for hver av komponentene. Antall komponenter bestemmes av integeren i stationInfo[][x]
        for i in range(0,stationInfo[x].nmrOfMeasurements,1):
            komponentXpath  = '//span[@id="ctl00_cph_Map_ctl00_gwStation_ctl0%d_Label1"]/text()'%(i+2)
            komponent[i]       = tree.xpath(komponentXpath)[0]
            
            verdierXpath    ='//span[@id="ctl00_cph_Map_ctl00_gwStation_ctl0%d_Label2"]/text()'%(i+2)
            timestamp       = correctTimestamp(tree.xpath(verdierXpath)[0])
            verdi[i]      = tree.xpath(verdierXpath)[1]
            verdi[i]      = verdi[i].replace(",", ".")
            if verdi[i] == "-":
                verdi[i] = "-99"
            datodognmiddel  = tree.xpath(verdierXpath)[2]
            verdidognmiddel = tree.xpath(verdierXpath)[3]
            enhet           = tree.xpath(verdierXpath)[4].encode('iso-8859-1')
            print komponent[i] + " " + timestamp + " " + verdi[i] + " " + datodognmiddel + " " + verdidognmiddel +" " + enhet


        try:
            with connection.cursor() as cursor:
                tiden = tiden + " " + timestamp +":00"
                print tiden
                # Create a new record
                #sql1    ="INSERT INTO %s (`timestamp`" %(stationInfo[x].tblName
                #sql2    ="VALUES ('%s'" %tiden
                
                #sql = "INSERT INTO %s (`timestamp`) VALUES ('%s')" %(stationInfo[x].tblName, tiden)
                #print sql
                #cursor.execute(sql)
                for i in range(0, stationInfo[x].nmrOfMeasurements,1):
                    #sql = "INSERT INTO %s (`timestamp`, `NO2`) VALUES ('1000-00-00 10:00:00', 20)" %(stationInfo[x].tblName)
                    column = komponent[i]
                    if column == "PM2.5":
                        column = "PM2"
                    sql = "INSERT INTO %s (`timestamp`, `%s`) VALUES ('%s', %s)" %(stationInfo[x].tblName + column, column, tiden, verdi[i])
#                    sql1    += ",`" + column + "`"
#                    sql2    += ",'" + verdi[i] + "'"
                    logging.debug(sql)
                    cursor.execute(sql)
                    logging.debug("Insertion successful")
#                sql1 +=") "
#                sql2 += ")"
#                sql = sql1 + sql2
#                logging.debug(sql)
#                cursor.execute(sql)
#logging.debug("Insertion successful")
        except:
            logging.error("MySQL Error, probably because of already existing timestamp")

    connection.close()

# -- coding: utf-8 --
from lxml import html
import requests
from setup import setupStations, getConnection

import pymysql.cursors


import schedule
import time
import datetime


# Fyller inn URL, antall målinger og tabellnavn per stasjon
stationInfo = setupStations()


#Kobler til mysql database
connection = getConnection()


#Går igjennom for hver stasjon
for x in range(0,len(stationInfo),1):
    #Henter dagens dato
    tiden = datetime.date.today()
    tiden = tiden.strftime('%Y-%m-%d')
    
    #Henter måledata
    page = requests.get(stationInfo[x].url)
    tree = html.fromstring(page.content)
    
    stationNameXpath = '//span[@id="ctl00_cph_Text_ctl00_lTitle"]/text()'
    stationName = tree.xpath(stationNameXpath)[0].encode('iso-8859-1')
    print stationName
    
    komponent = [None for _ in range(stationInfo[x].nmrOfMeasurements)]
    verdi = [None for _ in range(stationInfo[x].nmrOfMeasurements)]
    
    # Går igjennom nettsiden og henter ut verdier for hver av komponentene. Antall komponenter bestemmes av integeren i stationInfo[][x]
    for i in range(2,2+stationInfo[x].nmrOfMeasurements,1):
        komponentXpath  = '//span[@id="ctl00_cph_Map_ctl00_gwStation_ctl0%d_Label1"]/text()'%i
        komponent[i-2]       = tree.xpath(komponentXpath)[0]
        
        verdierXpath    ='//span[@id="ctl00_cph_Map_ctl00_gwStation_ctl0%d_Label2"]/text()'%i
        timestamp       = tree.xpath(verdierXpath)[0]
        verdi[i-2]      = tree.xpath(verdierXpath)[1]
        verdi[i-2]      = verdi[i-2].replace(",", ".")
        if verdi[i-2] == "-":
            verdi[i-2] = "-99"
        datodognmiddel  = tree.xpath(verdierXpath)[2]
        verdidognmiddel = tree.xpath(verdierXpath)[3]
        enhet           = tree.xpath(verdierXpath)[4].encode('iso-8859-1')
        print komponent[i-2] + " " + timestamp + " " + verdi[i-2] + " " + datodognmiddel + " " + verdidognmiddel +" " + enhet


    try:
        with connection.cursor() as cursor:
            tiden = tiden + " " + timestamp +":00"
            print tiden
            # Create a new record
            sql = "INSERT INTO %s (`timestamp`) VALUES ('%s')" %(stationInfo[x].tblName, tiden)
            print sql
            cursor.execute(sql)
            for i in range(0, stationInfo[x].nmrOfMeasurements,1):
                #sql = "INSERT INTO %s (`timestamp`, `NO2`) VALUES ('1000-00-00 10:00:00', 20)" %(stationInfo[x].tblName)
                column = komponent[i]
                if column == "PM2.5":
                    column = "PM2"
                
                sql = "UPDATE %s SET %s = %s WHERE (`timestamp`) = ('%s')" %(stationInfo[x].tblName, column, verdi[i], tiden)
                print sql
                cursor.execute(sql)
    except:
        print "MySQL Error"

connection.close()

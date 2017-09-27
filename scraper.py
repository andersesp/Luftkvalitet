# -- coding: utf-8 --
from lxml import html
import requests



import schedule
import time
import datetime

dim1, dim2 = 12, 2

stationInfo = [[0 for x in range(dim2)] for y in range(dim1)]


#Alnabru
stationInfo[0][0]   = "http://www.luftkvalitet.info/home/overview.aspx?type=2&topic=1&id=%7b7a08e76a-ce4f-4157-8134-e751186decdb%7d"
stationInfo[0][1]   = 3

#Breivoll
stationInfo[1][0]   = "http://www.luftkvalitet.info/home/overview.aspx?type=2&topic=1&id=%7bc76eb90f-4940-463d-94b6-a836c0829bce%7d"
stationInfo[1][1]   = 3

#Bygdøy Alle
stationInfo[2][0]   = "http://www.luftkvalitet.info/home/overview.aspx?type=2&topic=1&id=%7b002b3811-c249-4b4a-b5db-38a6189f79bc%7d"
stationInfo[2][1]   = 3

#Grønland
stationInfo[3][0]   = "http://www.luftkvalitet.info/home/overview.aspx?type=2&topic=1&id=%7b9f6b3149-209a-4e02-836c-c865c5e306f6%7d"
stationInfo[3][1]   = 3

#Hjortnes
stationInfo[4][0]   = "http://www.luftkvalitet.info/home/overview.aspx?type=2&topic=1&id=%7bE255C6C8-BCDC-BAD1-ADD6-F9855EBA1F79%7d"
stationInfo[4][1]   = 3

#Kirkeveien
stationInfo[5][0]   = "http://www.luftkvalitet.info/home/overview.aspx?type=2&topic=1&id=%7ba32be2e7-f071-4706-b8ec-556b5e187552%7d"
stationInfo[5][1]   = 4

#Manglerud
stationInfo[6][0]   = "http://www.luftkvalitet.info/home/overview.aspx?type=2&topic=1&id=%7b71e1836a-dc9a-4a54-bcfd-48493f9632eb%7d"
stationInfo[6][1]   = 3

#RV4, Aker Sykehus
stationInfo[7][0]   = "http://www.luftkvalitet.info/home/overview.aspx?type=2&topic=1&id=%7b766e5a7e-5074-4429-bb75-e0bb936ef7ab%7d"
stationInfo[7][1]   = 3

#Skøyen
stationInfo[8][0]   = "http://www.luftkvalitet.info/home/overview.aspx?type=2&topic=1&id=%7b738b6ba5-5fb0-4b81-aacc-d8020cebb0cd%7d"
stationInfo[8][1]   = 1

#Smestad
stationInfo[9][0]   = "http://www.luftkvalitet.info/home/overview.aspx?type=2&topic=1&id=%7bcd1e3904-029d-476b-bd2f-25e847bd2669%7d"
stationInfo[9][1]   = 3

#Sofienbergparken
stationInfo[10][0]  = "http://www.luftkvalitet.info/home/overview.aspx?type=2&topic=1&id=%7b4c308d8e-dba8-4f9f-8730-f083da14ae01%7d"
stationInfo[10][1]  = 2

#Åkerbergveien
stationInfo[11][0]  = "http://www.luftkvalitet.info/home/overview.aspx?type=2&topic=1&id=%7bc8b59bec-8bc6-4a63-a9b4-dc92b0178043%7d"
stationInfo[11][1]  = 2


for x in range(0,len(stationInfo),1):
    #Henter måledata
    page = requests.get(stationInfo[x][0])
    tree = html.fromstring(page.content)

    stationNameXpath = '//span[@id="ctl00_cph_Text_ctl00_lTitle"]/text()'
    stationName = tree.xpath(stationNameXpath)[0].encode('iso-8859-1')
    print stationName

    for i in range(2,2+stationInfo[x][1],1):
        komponentXpath  = '//span[@id="ctl00_cph_Map_ctl00_gwStation_ctl0%d_Label1"]/text()'%i
        komponent       = tree.xpath(komponentXpath)[0]

        verdierXpath    ='//span[@id="ctl00_cph_Map_ctl00_gwStation_ctl0%d_Label2"]/text()'%i
        timestamp       = tree.xpath(verdierXpath)[0]
        verdi           = tree.xpath(verdierXpath)[1]
        datodognmiddel  = tree.xpath(verdierXpath)[2]
        verdidognmiddel = tree.xpath(verdierXpath)[3]
        enhet           = tree.xpath(verdierXpath)[4].encode('iso-8859-1')
        print komponent + " " + timestamp + " " + verdi + " " + datodognmiddel + " " + verdidognmiddel +" " + enhet


#verdiXpath = '//span[@id="ctl00_cph_Map_ctl00_gwStation_ctl02_Label2"]



#stationID = []
#for i in range(2,14,1):
#    stationID.append(i)
#
#
#stationName =[]
#stationStatus = []
#
#for i in stationID:
#    
#    if i < 10:
#        namexpath = '//a[@id="ctl00_cph_Map_ctl00_gwArea_ctl0%d_hlStation2"]/text()' %i
#            airQxpath = '//span[@id="ctl00_cph_Map_ctl00_gwArea_ctl0%d_Label2"]/text()' %i
#        else:
#            namexpath = '//a[@id="ctl00_cph_Map_ctl00_gwArea_ctl%d_hlStation2"]/text()' %i
#            airQxpath = '//span[@id="ctl00_cph_Map_ctl00_gwArea_ctl%d_Label2"]/text()' %i
#    name = tree.xpath(namexpath)
#        nameString = name[0]	# Her den i hvertfall av type string, men fortsatt feil encoding
#        stationName.append(nameString)
#        stationStatus.append(tree.xpath(airQxpath))
#
#
#
##Fikser encoding
#for i in range (len(stationName)):
#    stationName[i] = stationName[i].encode('iso-8859-1')
#        stationStatus[i][0] = stationStatus[i][0].encode('iso-8859-1')
#        stationStatus[i][1] = stationStatus[i][1].encode('iso-8859-1')
#    
#    #Printer til terminal
#    for i in range(len(stationName)):
#        print stationName[i] + " luftforurensning : " + stationStatus[i][1]
#    
#    #Twitrer hvis det er høy forurensning
#    for i in range(len(stationName)):
#        if (stationStatus[i][1] != "Lite" and stationStatus[i][1] !="Ingen data"):
#            streng = "Forurensningnivå i " + stationName[i] + ": " +stationStatus[i][1] + "\n @AndersEspeseth"
#            print streng
#            api.update_status(streng)
#
#
#
#schedule.every(5).minutes.do(job)
#schedule.every(30).minutes.do(job2)
#
#while 1:
#    schedule.run_pending()
#    time.sleep(1)



#REF

#https://chatbotslife.com/create-a-simple-twitter-bot-with-python-and-tweepy-60ff5d4d3ad9
#http://www.luftkvalitet.info/home/overview.aspx?type=1&topic=1&id=%7b48fd69aa-76f7-4883-8bbb-5ba79c3879ea%7d

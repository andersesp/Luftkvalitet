 # -- coding: utf-8 -- 
from lxml import html
import requests

import tweepy
from secrets import *

import schedule
import time
import datetime


def job():
    #Twitter setup, må dette gjøres på nytt dersom man benytter sleep?
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)


    #Henter måledata
    page = requests.get("http://www.luftkvalitet.info/home/overview.aspx?type=1&topic=1&id=%7b48fd69aa-76f7-4883-8bbb-5ba79c3879ea%7d")
    tree = html.fromstring(page.content)

    stationID = []
    for i in range(2,14,1):
        stationID.append(i)


    stationName =[]
    stationStatus = []

    for i in stationID:
        
        if i < 10:
            namexpath = '//a[@id="ctl00_cph_Map_ctl00_gwArea_ctl0%d_hlStation2"]/text()' %i
            airQxpath = '//span[@id="ctl00_cph_Map_ctl00_gwArea_ctl0%d_Label2"]/text()' %i
        else:
            namexpath = '//a[@id="ctl00_cph_Map_ctl00_gwArea_ctl%d_hlStation2"]/text()' %i
            airQxpath = '//span[@id="ctl00_cph_Map_ctl00_gwArea_ctl%d_Label2"]/text()' %i
        name = tree.xpath(namexpath)
        nameString = name[0]	# Her den i hvertfall av type string, men fortsatt feil encoding
        stationName.append(nameString)
        stationStatus.append(tree.xpath(airQxpath))
        #print tree.xpath(airQxpath)
        #print nameString


    #Fikser encoding
    for i in range (len(stationName)):
        stationName[i] = stationName[i].encode('iso-8859-1')
        stationStatus[i][0] = stationStatus[i][0].encode('iso-8859-1')
        stationStatus[i][1] = stationStatus[i][1].encode('iso-8859-1')

    #Printer til terminal
    for i in range(len(stationName)):
        print stationName[i] + " luftforurensning : " + stationStatus[i][1]

    #Twitrer hvis det er høy forurensning
    for i in range(len(stationName)):
        if (stationStatus[i][1] != "Lite" and stationStatus[i][1] !="Ingen data"):
            streng = "Forurensningnivå i " + stationName[i] + ": " +stationStatus[i][1] + "\n @AndersEspeseth"
            print streng
            api.update_status(streng)

def job2():
    #Twitter setup, må dette gjøres på nytt dersom man benytter sleep?
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)
    tiden = datetime.datetime.now()
    tiden = tiden.strftime('%H:%M %m/%d/%Y')
    streng = "Jeg lever @AndersEspeseth " + tiden
    
    api.update_status(streng)

schedule.every(60*10).minutes.do(job)
schedule.every(60*3).minutes.do(job2)

while 1:
    schedule.run_pending()
    time.sleep(1)



#REF

#https://chatbotslife.com/create-a-simple-twitter-bot-with-python-and-tweepy-60ff5d4d3ad9
#http://www.luftkvalitet.info/home/overview.aspx?type=1&topic=1&id=%7b48fd69aa-76f7-4883-8bbb-5ba79c3879ea%7d

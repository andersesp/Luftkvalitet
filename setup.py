# -- coding: utf-8 --
import pymysql.cursors

class Mstation:
    def __init__(self, url, nmrOfMeasurements, tblName):
        self.url                = url
        self.nmrOfMeasurements  = nmrOfMeasurements
        self.tblName            = tblName

# Definerer url'er, antall målinger per stasjon og databasenavn
def setupStations():
    dim1, dim2 = 12, 3
    
    stationInfo = [[0 for x in range(dim2)] for y in range(dim1)]
    
    #Alnabru
    stationInfo[0]      = Mstation("http://www.luftkvalitet.info/home/overview.aspx?type=2&topic=1&id=%7b7a08e76a-ce4f-4157-8134-e751186decdb%7d", 3, "alnabru_tbl")
    
    #Breivoll
    stationInfo[1]      = Mstation("http://www.luftkvalitet.info/home/overview.aspx?type=2&topic=1&id=%7bc76eb90f-4940-463d-94b6-a836c0829bce%7d", 3, "breivoll_tbl")
    
    #Bygdøy Alle
    stationInfo[2]      = Mstation("http://www.luftkvalitet.info/home/overview.aspx?type=2&topic=1&id=%7b002b3811-c249-4b4a-b5db-38a6189f79bc%7d", 3, "bygdoy_tbl")
    
    #Grønland
    stationInfo[3]      = Mstation("http://www.luftkvalitet.info/home/overview.aspx?type=2&topic=1&id=%7b9f6b3149-209a-4e02-836c-c865c5e306f6%7d", 3, "gronland_tbl")
    
    #Hjortnes
    stationInfo[4]      = Mstation("http://www.luftkvalitet.info/home/overview.aspx?type=2&topic=1&id=%7bE255C6C8-BCDC-BAD1-ADD6-F9855EBA1F79%7d", 3,  "hjortnes_tbl")
    
    #Kirkeveien
    stationInfo[5]      = Mstation("http://www.luftkvalitet.info/home/overview.aspx?type=2&topic=1&id=%7ba32be2e7-f071-4706-b8ec-556b5e187552%7d", 4, "kirkeveien_tbl")
    
    #Manglerud
    stationInfo[6]      = Mstation("http://www.luftkvalitet.info/home/overview.aspx?type=2&topic=1&id=%7b71e1836a-dc9a-4a54-bcfd-48493f9632eb%7d", 3,  "manglerud_tbl")
    
    #RV4, Aker Sykehus
    stationInfo[7]      = Mstation("http://www.luftkvalitet.info/home/overview.aspx?type=2&topic=1&id=%7b766e5a7e-5074-4429-bb75-e0bb936ef7ab%7d", 3, "rv4_tbl")
    
    #Skøyen
    stationInfo[8]      = Mstation("http://www.luftkvalitet.info/home/overview.aspx?type=2&topic=1&id=%7b738b6ba5-5fb0-4b81-aacc-d8020cebb0cd%7d", 1, "skoyen_tbl")
    
    #Smestad
    stationInfo[9]      = Mstation("http://www.luftkvalitet.info/home/overview.aspx?type=2&topic=1&id=%7bcd1e3904-029d-476b-bd2f-25e847bd2669%7d", 3, "smestad_tbl")
    
    #Sofienbergparken
    stationInfo[10]     = Mstation("http://www.luftkvalitet.info/home/overview.aspx?type=2&topic=1&id=%7b4c308d8e-dba8-4f9f-8730-f083da14ae01%7d", 2, "sofienbergparken_tbl")
    
    #Åkerbergveien
    stationInfo[11]     = Mstation("http://www.luftkvalitet.info/home/overview.aspx?type=2&topic=1&id=%7bc8b59bec-8bc6-4a63-a9b4-dc92b0178043%7d", 2, "akerbergveien_tbl")
    
    return stationInfo

def getConnection():
    connection = pymysql.connect(host='localhost',
                             user = 'python',
                             password = 'raspberry',
                             db = 'timesverdier',
                             charset='utf8mb4',
                             cursorclass = pymysql.cursors.DictCursor,
                             autocommit = True)
    return connection

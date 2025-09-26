"""
python GetStocksByIndustryClassification.py 
"""
import sys
import os 
import time
import re
import sys
import csv
import ssl
import requests
#import urllib.parse
#import urllib.request
from bs4 import BeautifulSoup


if len(sys.argv) < 3 :
    print("You need input two parameter(fmt : directory filename)")
    print("syntax : C:\python GetStocksByIndustryClassification.py IndustryClassification\\ ic20221102.txt ")
    sys.exit()

theSaveFileDir = sys.argv[1]
#theInputFile = sys.argv[2]
#theOutputFile = "insertcmd.txt"
theInsertCmd = "insert into stocks_belongto_industry_classification (classificationType, classificationCode, stockNo, stockName) values ("
insertCnt = 0
errorCnt = 0

# for windows now (2022.11.02)
#saveFileDir = "IndustryClassification\\"
#fileName = "test.txt"
theSaveFileDir = sys.argv[1]
theInputFileName = sys.argv[2]
theOutputFileName = "insert_cmd.txt"



#with open(theInputFileName, 'r', encoding = 'cp950') as theInputFile :
with open(theInputFileName, 'r', encoding = 'utf-8') as theInputFile :
    theOutputFile = open(theSaveFileDir + theOutputFileName, 'w', encoding = 'utf-8')
    for eachLine in theInputFile :
        theList = eachLine.split(",") 
        print(theList)
        theClassificationType = theList[0]
        theClassificationCode = theList[1]
        theHyperlink = theList[2].replace("\n", "")

    #    theOutputFileName = theSaveFileDir + theClassificationCode + ".txt"
    #    print(theOutputFileName)
#        theOutputFile = open(prnData, 'w')

        print('處理網頁 : ' + theClassificationCode)
#        theOutputFile = open(theOutputFileName, 'w', encoding = 'utf-8')
        ssl._create_default_https_context = ssl._create_unverified_context
#        url = "https://sjmain.esunsec.com.tw/z/zh/zha/zha.djhtm"

        user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
        headers = {'User-Agent': user_agent}

        resp = requests.get(theHyperlink, headers = headers)
#       windows platform : big5 ; linux platform : utf-8        
        resp.encoding = 'big5'

        soup = BeautifulSoup(resp.text, 'lxml')
        theTable = soup.find(lambda tag: tag.name=='table' and tag.has_key('id') and tag['id']=="oMainTable")
#        print("script: ", theTable.td.script.string)
#        print(soup)
        for sibling in theTable.tr.next_siblings:
            theTR = BeautifulSoup(repr(sibling), 'lxml')
            tds = theTR.findAll(lambda tag: tag.name=='td')
            for theTD in theTR.findAll(lambda tag: tag.name=='td') :  
                theContent = str(theTD)
                print(theContent)
                if theContent.find("GenLink2stk('") >= 0 :
                    thePos1 = theContent.find("GenLink2stk('") + 12
                    thePos2 = theContent.find(");")
                    print(str(thePos1), str(thePos2))
#                    theOutputFile.write(str(theTD))
                    theValues = theInsertCmd + "'" + theClassificationType + "', '" + theClassificationCode + \
                        "','" + theContent[thePos1+3:thePos2] + ");"
                    theOutputFile.write(theValues)
                    theOutputFile.write('\n')
        
    theOutputFile.close()















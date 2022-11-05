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
theInputFile = sys.argv[2]
theOutputFile = ""
insertCnt = 0
errorCnt = 0

# for windows now (2022.11.02)
#saveFileDir = "IndustryClassification\\"
#fileName = "test.txt"
theSaveFileDir = sys.argv[1]
theInputFileName = sys.argv[2]

# Step01
# 先組出要抓檔的分類、來源網址 (Data from file: IC_StocksAddressList.txt)
#
#with open(theSaveFileDir + theInputFileName, 'r', encoding = 'CP950') as infile :
with open(theInputFileName, 'r', encoding = 'utf-8') as theInputFile :
    for eachLine in theInputFile :
        theList = eachLine.split(",") 
        print(theList)
        theOutputFileName = theSaveFileDir + theList[1] + ".txt"
        theHyperlink = theList[2].replace("\n", "")
        print(theOutputFileName)
#        theOutputFile = open(prnData, 'w')

        print('處理網頁 : ' + theList[1])
        theOutputFile = open(theOutputFileName, 'w')
        ssl._create_default_https_context = ssl._create_unverified_context
        url = "https://sjmain.esunsec.com.tw/z/zh/zha/zha.djhtm"

        user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
        headers = {'User-Agent': user_agent}

        resp = requests.get(theHyperlink, headers = headers)
        resp.encoding = 'cp950'

        soup = BeautifulSoup(resp.text, 'lxml')
        theTable = soup.find(lambda tag: tag.name=='table' and tag.has_key('id') and tag['id']=="oMainTable")
#        print("script: ", theTable.td.script.string)
#        print(soup)
        for sibling in theTable.tr.next_siblings:
            theTR = BeautifulSoup(repr(sibling), 'lxml')
            tds = theTR.findAll(lambda tag: tag.name=='td')
            for theTD in theTR.findAll(lambda tag: tag.name=='td') :
                print(theTD)
                theOutputFile.write(str(theTD))
                theOutputFile.write('\n')

        
        theOutputFile.close()















"""
GetStocksByIndustryClassification.py 
Syntax:
    windows : python GetStocksByIndustryClassification.py IndustryClassification\ IC_StocksAddressList.txt
    linux   : python3 GetStocksByIndustryClassification.py IndustryClassification/ IC_StocksAddressList.txt
    NOTE    : IC_StocksAddressList.txt 資料來至 stocksdb -> industry_classification (table)
20221106 Windows & Linux platform both run OK
20221108 配合table欄位名稱修改調整sql command
"""
import os 
import re
import sys
import csv
import ssl
import time
import requests
#from time import sleep
from bs4 import BeautifulSoup

if len(sys.argv) < 3 :
    print("You need input two parameter(fmt : directory inputfile)")
    print("syntax : C:\python GetStocksByIndustryClassification.py IndustryClassification\\ ic20221102.txt ")
    sys.exit()

THE_INSERT_CMD = "insert into stocks_belongto_industry_classification " \
    "(classification_type, classification_code, stock_no, stock_name) values ("
theSaveFileDir = sys.argv[1]
theInputFileName = sys.argv[2]
theOutputFileName = "Insert_stocks_belongto_industry_classification_cmd.txt"

with open(theInputFileName, 'r', encoding = 'utf-8') as theInputFile :
    theOutputFile = open(theSaveFileDir + theOutputFileName, 'w', encoding = 'utf-8')
    for eachLine in theInputFile :
        theList = eachLine.split(",") 
        print(theList)
        theClassificationType = theList[0]
        theClassificationCode = theList[1]
        theHyperlink = theList[2].replace("\n", "") # 沒去掉換行符號,程式會有問題

        print('處理網頁 : ' + theClassificationCode)
        ssl._create_default_https_context = ssl._create_unverified_context
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
        headers = {'User-Agent': user_agent}

        resp = requests.get(theHyperlink, headers = headers)
        resp.encoding = 'big5' # 本網站網頁是big5編碼

        time.sleep(2) # 暫停2秒,以免頻繁讀取被封鎖

        soup = BeautifulSoup(resp.text, 'lxml')
        theTable = soup.find(lambda tag: tag.name=='table' and tag.has_key('id') and tag['id']=="oMainTable")
        for sibling in theTable.tr.next_siblings:
            theTR = BeautifulSoup(repr(sibling), 'lxml')
            tds = theTR.findAll(lambda tag: tag.name=='td')
            for theTD in theTR.findAll(lambda tag: tag.name=='td') :  
                theContent = str(theTD)
                print(theContent)
#               未來玉山證券網站有改程式,此處要配合調整                
                if theContent.find("GenLink2stk('") >= 0 :
                    thePos1 = theContent.find("GenLink2stk('") + 12 # 12為搜尋字串長度
                    thePos2 = theContent.find(");")
                    print(str(thePos1), str(thePos2))
                    theOutputString = THE_INSERT_CMD + "'" + theClassificationType + \
                        "','" + theClassificationCode + \
                        "','" + theContent[(thePos1 + 3) : thePos2] + ");"
                    theOutputFile.write(theOutputString)
                    theOutputFile.write('\n')
        
    theOutputFile.close()

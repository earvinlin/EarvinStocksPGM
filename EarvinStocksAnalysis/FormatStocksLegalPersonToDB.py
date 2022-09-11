"""
讀取法人買賣與持股資料資料，並將之格式化為Insert SQL Command
資料來源：https://jsjustweb.jihsun.com.tw/z/zc/zcl/zcl.djhtm?a=2049&c=2021-9-7&d=2022-9-7
"""
import re
import sys
import csv
import bs4
import platform
import urllib.parse
import urllib.request

theInsertCmd ="INSERT INTO STOCKS_LEGAL_PERSON (DATE, FOREIGN_TRADE, "\
    "SIT_AND_CB_TRADE, SELF_EMPLOYED_TRADE, SUM_TRADE, FOREIGN_ESTIMATE, " \
    "SIT_AND_CB_ESTIMATE, SELF_EMPLOYED_ESTIMATE, SUM_ESTIMATE, " \
    "FOREIGN_PROPORTION, THREE_LEGAL_PERSON_PROPORTION) VALUES ("

def NotEmpty(s) :
  return s and s.strip()

if len(sys.argv) < 2 :
    print("You need input one parameter(fmt : theFilename ))")
    print("syntax : C:\python FormatStocksLegalPersonToDB.py 法人_0050_20200101-20220909.htm ")
    sys.exit()

pattern = r'\d*\/\d*\/\d*'
theInputFile = sys.argv[1]
theOutputFile = theInputFile[:theInputFile.find(".")] + ".txt"
theLoadFileDir = ""
theSaveFileDir = ""
if platform.system() == "Windows" :
    theLoadFileDir = "Data\\LEGAL\\"
    theSaveFileDir = "Data\\LEGAL\\SQL\\"
else :
    theLoadFileDir = "./Data/LEGAL/"
    theSaveFileDir = "./Data/LEGAL/SQL/"

try :
    outfile = open(theSaveFileDir + theOutputFile, 'w')
    stockData = open(theLoadFileDir + theInputFile, 'r')	# 預設以系統編碼開啟
    objSoup = bs4.BeautifulSoup(stockData, 'html.parser')
    objForm = objSoup.find('form')
    objTables = objForm.find_all('table')

    for c in objTables[1].children:
        if c.name == "tr" :
            d = c.text.split('\n')
            theFilter = filter(NotEmpty, d)
            theList = list(theFilter)
            if len(theList) > 1 :
                match = re.findall(pattern, theList[0])
                if len(match) > 0 :
                    theString =""
                    for i in range(len(theList)) :
                        theList[i] = theList[i].replace('-', '0')
                        theList[i] = theList[i].replace('/', '')
                        theList[i] = theList[i].replace(',', '')
                        theList[i] = theList[i].replace('%', '')
                        theList[i] = theList[i].strip()
                        theString += theList[i] + ", "
#                   組出Insert Command
                    if len(theString) > 0 :
                        theString = theInsertCmd + \
                            theString[0 : len(theString) - 2] + "); "

                    print("theString= " + theString)
                    outfile.write(theString + "\n")

    print('資料儲存完成!!')
    stockData.close()
    outfile.close()

except IOError as err :
    print('Fie error : ' + str(err))

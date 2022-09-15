"""
【程式功能說明】
讀取法人買賣與持股資料資料，並將之格式化為Insert SQL Command
資料來源：https://jsjustweb.jihsun.com.tw/z/zc/zcl/zcl.djhtm?a=2049&c=2021-9-7&d=2022-9-7

<NOTE>
(01)
讀取資料放置處，執行前需確認程式(GetTWStocksLegalPerson.py)抓的資料有放在下列路徑：(以windows平台為例)
==> theLoadFileDir = "Data\LEGAL\20190101-20191231\"
產生SQL Command的資料放置處：(以windows平台為例)
==> theSaveFileDir = "Data\LEGAL\\SQL\"

(02)
如果資料來源是在windows平台抓取，則直接使用下列開檔指令(使用預設編碼)
inputfile = open(theLoadRelativePath, 'r')	# 預設以系統編碼(cp950)開啟
如果資料來源是在imac/linux平台抓取，則直接使用下列開檔指令(即需指定編碼為utf-8)
inputfile = open(theLoadRelativePath, 'r', encoding='utf-8')	# utf-8編碼開啟
"""
import os 
import re
import sys
import csv
import bs4
import platform
import urllib.parse
import urllib.request

theInsertCmd ="INSERT INTO STOCKS_LEGAL_PERSON (DATE, STOCK_NO, FOREIGN_TRADE, "\
    "SIT_AND_CB_TRADE, SELF_EMPLOYED_TRADE, SUM_TRADE, FOREIGN_ESTIMATE, " \
    "SIT_AND_CB_ESTIMATE, SELF_EMPLOYED_ESTIMATE, SUM_ESTIMATE, " \
    "FOREIGN_PROPORTION, THREE_LEGAL_PERSON_PROPORTION) VALUES ("

def NotEmpty(s) :
  return s and s.strip()

"""
if len(sys.argv) < 2 :
    print("You need input one parameter(fmt : theFilename ))")
    print("syntax : C:\python FormatStocksLegalPersonToDB.py 法人_0050_20200101-20220909.htm ")
    sys.exit()
"""

thePattern = r'\d*\/\d*\/\d*'
theInputFile = ""   
theOutputFile = ""
theLoadFileDir = ""
theSaveFileDir = ""
theStockNo = ""
if platform.system() == "Windows" :
#   讀取檔案的來原路徑    
    theLoadFileDir = "DATA\\LEGAL\\HTM\\20120101-20121231_utf8\\"
#    theLoadFileDir = "Data\\LEGAL\\"   
    theSaveFileDir = "Data\\LEGAL\\SQL\\"
else :
    theLoadFileDir = "./Data/LEGAL/"
    theSaveFileDir = "./Data/LEGAL/SQL/"

try :
    theAllFiles = os.listdir(theLoadFileDir)
    for theFile in theAllFiles :
        theLoadRelativePath = os.path.join(theLoadFileDir, theFile)
        if os.path.isfile(theLoadRelativePath) :
            print("處理檔案：", theFile)
            thePosition = theFile.find("_")
            theStockNo = theFile[(thePosition + 1) : (thePosition + 5)] 
#            print("檔案：", theStockNo)
            theOutputFile = theFile[: len(theFile) - 4] + ".txt"
            theSaveRelativePath = os.path.join(theSaveFileDir, theOutputFile)
            print("outfile: " + theOutputFile)
# 來源檔案是由windows平台抓取則編碼為cp950；若為imac/linux平台則編碼為utf-8。
# 所以程式讀檔前要注意設定的編碼(encoding)            
#            inputfile = open(theLoadRelativePath, 'r')	# 預設以系統(windows)編碼cp950開啟
            inputfile = open(theLoadRelativePath, 'r', encoding='utf-8')	# imac/linux編碼為utf-8
            outfile = open(theSaveRelativePath, 'w')
            objSoup = bs4.BeautifulSoup(inputfile, 'html.parser')
            objForm = objSoup.find('form')
            objTables = objForm.find_all('table')

            for c in objTables[1].children:
                if c.name == "tr" :
                    d = c.text.split('\n')
                    theFilter = filter(NotEmpty, d)
                    theList = list(theFilter)
                    if len(theList) > 1 :
                        isMatch = re.findall(thePattern, theList[0])
                        if len(isMatch) > 0 :
                            theString =""
                            for i in range(len(theList)) :
#                               日期(i == 0)後要先加上股票代號                                
                                if i == 1 :
                                    theString += "'" + theStockNo + "', "

                                theList[i] = theList[i].replace('-', '0')
                                theList[i] = theList[i].replace('/', '')
                                theList[i] = theList[i].replace(',', '')
                                theList[i] = theList[i].replace('%', '')
                                theList[i] = theList[i].strip()
                                theString += theList[i] + ", "
                            if len(theString) > 0 :
                                theString = theInsertCmd + \
                                    theString[0 : len(theString) - 2] + "); "
#                            print("theString= " + theString)
                            outfile.write(theString + "\n")
            inputfile.close()
            outfile.close()

    print('資料儲存完成!!')

except IOError as err :
    print('Fie error : ' + str(err))

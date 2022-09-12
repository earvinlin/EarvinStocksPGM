"""
【程式功能說明】
讀取法人買賣與持股資料資料，並將之格式化為Insert SQL Command
資料來源：https://jsjustweb.jihsun.com.tw/z/zc/zcl/zcl.djhtm?a=2049&c=2021-9-7&d=2022-9-7

<NOTE>
(01)
讀取資料放置處，執行前需確認程式(GetTWStocksLegalPerson.py)抓的資料有放在下列路徑：(以windows平台為例)
==> theLoadFileDir = "Data\\LEGAL\\20190101-20191231\\"
產生SQL Command的資料放置處：(以windows平台為例)
==> theSaveFileDir = "Data\\LEGAL\\SQL\\"

(02)
如果資料來源是在windows平台抓取，則直接使用下列開檔指令(使用預設編碼)
inputfile = open(theLoadRelativePath, 'r')	# 預設以系統編碼開啟
如果資料來源是在imac/linux平台抓取，則直接使用下列開檔指令(即需指定編碼為utf-8)
inputfile = open(theLoadRelativePath, 'r', encoding='utf-8')	# utf-8編碼(for iMac/Linux)

"""
import os 
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
if platform.system() == "Windows" :
    theLoadFileDir = "Data\\LEGAL\\20200101-20220909\\"
    theSaveFileDir = "Data\\LEGAL\\SQL\\"
else :
    theLoadFileDir = "./Data/LEGAL/"
    theSaveFileDir = "./Data/LEGAL/SQL/"

try :
    files = os.listdir(theLoadFileDir)
    for theFile in files :
        theLoadRelativePath = os.path.join(theLoadFileDir, theFile)
        if os.path.isfile(theLoadRelativePath) :
            print("檔案：", theFile)
            theOutputFile = theFile[: len(theFile) - 4] + ".txt"
            theSaveRelativePath = os.path.join(theSaveFileDir, theOutputFile)
            print("outfile: " + theOutputFile)
            inputfile = open(theLoadRelativePath, 'r')	# 預設以系統編碼開啟
#            inputfile = open(theLoadRelativePath, 'r', encoding='utf-8')	# utf-8編碼(for iMac/Linux)
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
                                theList[i] = theList[i].replace('-', '0')
                                theList[i] = theList[i].replace('/', '')
                                theList[i] = theList[i].replace(',', '')
                                theList[i] = theList[i].replace('%', '')
                                theList[i] = theList[i].strip()
                                theString += theList[i] + ", "
                            if len(theString) > 0 :
                                theString = theInsertCmd + \
                                    theString[0 : len(theString) - 2] + "); "
                            print("theString= " + theString)
                            outfile.write(theString + "\n")
            inputfile.close()
            outfile.close()

    print('資料儲存完成!!')

except IOError as err :
    print('Fie error : ' + str(err))

"""
取得法人買賣與持股資料資料
資料來源：https://jsjustweb.jihsun.com.tw/z/zc/zcl/zcl.djhtm?a=2049&c=2021-9-7&d=2022-9-7
"""
import re
import sys
import csv
import urllib.request
import urllib.parse
import ssl
import platform

if len(sys.argv) < 5 :
    print("You need input three parameter(fmt : theFilename theBeginDate theEndDate (fmt : yyyymmdd))")
    print("syntax : C:\python GetTWStocksLegalPerson.py STOCKS_LIST 20170401 20220401")
    sys.exit()

theInputFile = sys.argv[1]
theOutputFile = ""
theSaveFileDir = ""
if platform.system() == "Windows" :
    theSaveFileDir = "Data\\LEGAL\\"
else :
#    theSaveFileDir = "./Data/LEGAL/20170101-20171231(imac-utf8)/"
    theSaveFileDir = "./Data/LEGAL/" + sys.argv[4] + "/"

readCnt = 0

theBeginDate = sys.argv[2]
theBeginDate =  theBeginDate[:4] + "-" + theBeginDate[4:6] + "-" + theBeginDate[6:8]
theEndDate = sys.argv[3]
theEndDate = theEndDate[:4] + "-" + theEndDate[4:6] + "-" + theEndDate[6:8]

print("BeginDate= " + theBeginDate, ", EndDate= ", theEndDate)

ssl._create_default_https_context = ssl._create_unverified_context

try :
    twStocksList = open(theInputFile, 'r')	# 預設以系統編碼開啟
    theStocksList = twStocksList.readlines()
    for theStockNo in theStocksList :
        theStockNo = theStockNo.replace('\n', '')
#       url = "https://jsjustweb.jihsun.com.tw/z/zc/zcl/zcl.djhtm?a=2049&c=2021-9-7&d=2022-9-7"
        theURL = "https://jsjustweb.jihsun.com.tw/z/zc/zcl/zcl.djhtm?a=" + theStockNo + \
            "&c=" + theBeginDate + "&d=" + theEndDate
        print("URL= " + theURL)
        f = urllib.request.urlopen(theURL)
        
        theOutputFile = "法人_" + theStockNo + "_" + sys.argv[2] + \
            "-" + sys.argv[3] + ".htm"
        print('檔案名稱：' + theOutputFile)
        with open(theSaveFileDir + theOutputFile, 'w') as out :
#		    f.read()是byte型態，需解碼(decode)儲存成字串
#            out.write(f.read().decode('big5'))
            out.write(f.read().decode('cp950'))
        print('資料儲存完成!!')
    twStocksList.close()
except IOError as err :
    print('Fie error : ' + str(err))



import re
import sys
import urllib.request
import urllib.parse
#from bs4 import BeautifulSoup

if len(sys.argv) < 3 :
    print("You need input two parameter(fmt : yyyymmdd(西元日期) type(交易型態,值請檢視網頁原始檔))")
    print("syntax : C:\python 05_getTaiwanDataTsecMarginWithParams.py 20170405 MS ")
    sys.exit()

url = "http://www.tse.com.tw/exchangeReport/MI_MARGN?response=csv&date=" + sys.argv[1] + "&selectType=" + sys.argv[2]
#      http://www.tse.com.tw/exchangeReport/MI_MARGN?response=csv&date=20190524&selectType=MS
f = urllib.request.urlopen(url)

try :
    saveFileDir = "大盤融資融券\\"
    fileName = "大盤融資融券_" + sys.argv[1] + ".txt"
    print('檔案名稱：' + fileName)
    with open(saveFileDir + fileName, 'w') as out :
#		f.read()是byte型態，需解碼(decode)儲存成字串
        out.write(f.read().decode('big5'))

    print('資料儲存完成!!')
except IOError as err :
    print('Fie error : ' + str(err))

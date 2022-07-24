import re
import sys
import urllib.request
import urllib.parse
#from bs4 import BeautifulSoup
import ssl

if len(sys.argv) < 2 :
    print("You need input two parameter(fmt : theDate(yyyymmdd))")
    print("syntax : C:\python 01_taiwanDataTSECDataWithParams.py 20170501 ")
    sys.exit()

ssl._create_default_https_context = ssl._create_unverified_context
url = "https://www.twse.com.tw/indicesReport/MI_5MINS_HIST?response=csv&date=" + sys.argv[1]
# For Test
#(20211218 old) url = "http://www.tse.com.tw/indicesReport/MI_5MINS_HIST?response=csv&date=20200701"
#https://www.twse.com.tw/exchangeReport/FMTQIK?response=csv&date=20211218

print("url= " + url)
f = urllib.request.urlopen(url)

try :
    saveFileDir = "大盤指數\\"
    fileName = "大盤指數_" + sys.argv[1] + ".txt"
    print('檔案名稱：' + fileName)
    with open(saveFileDir + fileName, 'w') as out :
#		f.read()是byte型態，需解碼(decode)儲存成字串
        out.write(f.read().decode('big5'))

    print('資料儲存完成!!')
except IOError as err :
    print('Fie error : ' + str(err))

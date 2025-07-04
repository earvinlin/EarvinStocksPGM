import re
import sys
import urllib.request
import urllib.parse
#from bs4 import BeautifulSoup
import ssl

if len(sys.argv) < 3 :
    print("You need input two parameter(fmt : yyyymmdd(西元日期) type(交易型態,值請檢視網頁原始檔))")
    print("syntax : C:\python 05_getTaiwanDataTsecMarginWithParams.py 20170405 MS ")
    sys.exit()

ssl._create_default_https_context = ssl._create_unverified_context
url = "https://www.twse.com.tw/exchangeReport/MI_MARGN?response=csv&date=" + sys.argv[1] + "&selectType=" + sys.argv[2]
#      https://www.twse.com.tw/exchangeReport/MI_MARGN?response=csv&date=20211217&selectType=MS
f = urllib.request.urlopen(url)

try :
# 20250702 判斷程式是在何種作業系統執行以確認路徑撰寫方式
#    saveFileDir = "大盤融資融券\\"
    saveFileDir = ""
    if sys.platform == "darwin" or sys.platform == "linux" :
        saveFileDir = "大盤融資融券/"
    else :
        saveFileDir = "大盤融資融券\\"
# 20250702 --- END ---

    fileName = "大盤融資融券_" + sys.argv[1] + ".txt"
    print('檔案名稱：' + fileName)
    with open(saveFileDir + fileName, 'w') as out :
#		f.read()是byte型態，需解碼(decode)儲存成字串
        out.write(f.read().decode('big5'))

    print('資料儲存完成!!')
except IOError as err :
    print('Fie error : ' + str(err))

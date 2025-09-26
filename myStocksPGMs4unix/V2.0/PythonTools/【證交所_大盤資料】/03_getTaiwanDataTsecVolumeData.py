import re
import sys
import csv
import urllib.request
import urllib.parse
#from bs4 import BeautifulSoup
import ssl

if len(sys.argv) < 2 :
    print("You need input two parameter(fmt : theDate(yyyymmdd))")
    print("syntax : C:\python 03_getTaiwanDataTsecVolumeWithParams2.py 20170401 ")
    sys.exit()

# params = urllib.parse.urlencode({'query_year':sys.argv[1], 'query_month':sys.argv[2]}) #這是我自己的參數
# params = params.encode('big5')
#url = "https://www.twse.com.tw/exchangeReport/FMTQIK?response=csv&date=20211218"
ssl._create_default_https_context = ssl._create_unverified_context
#url = "https://www.twse.com.tw/exchangeReport/FMTQIK?response=csv&date=" + sys.argv[1]
url = "https://www.twse.com.tw/exchangeReport/FMTQIK?response=csv&date=" + sys.argv[1]

f = urllib.request.urlopen(url)

try :
# 20250702 判斷程式是在何種作業系統執行以確認路徑撰寫方式
#    saveFileDir = "大盤成交量\\"
    saveFileDir = ""
    if sys.platform == "darwin" or sys.platform == "linux" :
        saveFileDir = "大盤成交量/"
    else :
        saveFileDir = "大盤成交量\\"
# 20250702 --- END ---

    fileName = "大盤成交量_" + sys.argv[1] + ".txt"
    print('檔案名稱：' + fileName)
    with open(saveFileDir + fileName, 'w') as out :
#		f.read()是byte型態，需解碼(decode)儲存成字串
        out.write(f.read().decode('big5'))

    print('資料儲存完成!!')
except IOError as err :
    print('Fie error : ' + str(err))

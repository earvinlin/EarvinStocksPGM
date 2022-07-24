import re
import sys
import csv
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

if len(sys.argv) < 2 :
    print("You need input two parameter(fmt : theDate(yyyymmdd))")
    print("syntax : C:\python 03_getTaiwanDataTsecVolumeWithParams2.py 20170401 ")
    sys.exit()

# params = urllib.parse.urlencode({'query_year':sys.argv[1], 'query_month':sys.argv[2]}) #這是我自己的參數
# params = params.encode('big5')
#url = "http://www.tse.com.tw/ch/trading/exchange/FMTQIK/FMTQIK.php"
url = "http://www.tse.com.tw/exchangeReport/FMTQIK?response=csv&date=" + sys.argv[1]

f = urllib.request.urlopen(url)

try :
    fileName = "大盤成交量_" + sys.argv[1] + ".txt"
    print('檔案名稱：' + fileName)
    with open(fileName, 'w') as out :
#		f.read()是byte型態，需解碼(decode)儲存成字串
        out.write(f.read().decode('big5'))

    print('資料儲存完成!!')
except IOError as err :
    print('Fie error : ' + str(err))

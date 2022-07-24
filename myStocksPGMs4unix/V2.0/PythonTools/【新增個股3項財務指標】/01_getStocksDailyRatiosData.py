import re
import sys
import urllib.request
import urllib.parse
import ssl

if len(sys.argv) < 2 :
    print("You need input one parameter(fmt : theProcessDate(yyyymmdd))")
    print("syntax : C:\python 01_getStocksDailyRatiosData.py 20170501 ")
    sys.exit()

print("input-value= " + sys.argv[1] + "\n")

ssl._create_default_https_context = ssl._create_unverified_context
#      https://www.twse.com.tw/exchangeReport/BWIBBU_d?response=csv&date=20211217&selectType=ALL
#url = "http://www.tse.com.tw/exchangeReport/BWIBBU_d?response=csv&date=" + sys.argv[1] + "&selectType=ALL"
url = "https://www.twse.com.tw/exchangeReport/BWIBBU_d?response=csv&date=" + sys.argv[1] + "&selectType=ALL"
f = urllib.request.urlopen(url)
#print(f.read().decode('CP950'))

try :
    saveFileDir = "Files\\"
    fileName = "stocks_個股日本益比殖利率及股價淨值比-" + sys.argv[1] + ".txt"
    print('檔案名稱：' + fileName)
    with open(saveFileDir + fileName, 'w') as out :
#		f.read()是byte型態，需解碼(decode)儲存成字串
        out.write(f.read().decode('CP950'))

    print('資料儲存完成!!')
except IOError as err :
    print('Fie error : ' + str(err))


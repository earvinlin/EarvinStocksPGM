import re
import sys
import csv
import urllib.parse
import urllib.request
#from bs4 import BeautifulSoup
import ssl

"""
if len(sys.argv) < 2 :
    print("You need input two parameter(fmt : theDate(yyyymmdd))")
    print("syntax : C:\python 03_getTaiwanDataTsecVolumeWithParams2.py 20170401 ")
    sys.exit()
"""

ssl._create_default_https_context = ssl._create_unverified_context
url = "https://www.esunsec.com.tw/tw-market/z/ze/zeg/zeg_23.djhtm"

#f = urllib.request.urlopen(url)

#url = 'http://www.someserver.com/cgi-bin/register.cgi'
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
values = {'name': 'Michael Foord',
          'location': 'Northampton',
          'language': 'Python' }
headers = {'User-Agent': user_agent}

#data = urllib.parse.urlencode(values)
#data = data.encode('utf-8')
req = urllib.request.Request(url, headers=headers)
f = urllib.request.urlopen(req)

try :
    saveFileDir = "產業分類\\"
    fileName = "產業分類" + ".txt"
    print('檔案名稱：' + fileName)
    with open(saveFileDir + fileName, 'w') as out :
#		f.read()是byte型態，需解碼(decode)儲存成字串
        out.write(f.read().decode('utf-8'))

    print('資料儲存完成!!')
except IOError as err :
    print('Fie error : ' + str(err))

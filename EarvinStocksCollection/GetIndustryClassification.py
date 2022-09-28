import re
import sys
import csv
import ssl
import requests
#import urllib.parse
#import urllib.request
from bs4 import BeautifulSoup

"""
if len(sys.argv) < 2 :
    print("You need input two parameter(fmt : theDate(yyyymmdd))")
    print("syntax : C:\python 03_getTaiwanDataTsecVolumeWithParams2.py 20170401 ")
    sys.exit()
"""

HYPER_LINK = "https://sjmain.esunsec.com.tw"
ssl._create_default_https_context = ssl._create_unverified_context
# Source : 玉山證券，資料嵌在iframe
# iframe : https://sjmain.esunsec.com.tw/z/zh/zha/zha.djhtm
url = "https://sjmain.esunsec.com.tw/z/zh/zha/zha.djhtm"

user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
headers = {'User-Agent': user_agent}

resp = requests.get(url, headers=headers)
resp.encoding = 'cp950'

#soup = BeautifulSoup(resp.text, 'html.parser')
soup = BeautifulSoup(resp.text, 'lxml')
print("title: ", soup.title.text)

table = soup.find(lambda tag: tag.name=='table' and tag.has_key('id') and tag['id']=="oMainTable")
rows = table.findAll(lambda tag: tag.name=='tr')
icount = 0
for row in table.findAll("tr"):
#   只取「產業別」欄位
    if icount%2 == 0 :
        tds = row.find_all("td")
        for td in tds :
            industry = td.get_text()
            lnks = td.find_all("a")
            for lnk in lnks :
                industryGroupHyperlink = HYPER_LINK + lnk.get('href')
                print("v(" + str(icount) + ")= " + industry)
                print("industryGroupHyperlink= " + industryGroupHyperlink)
                break   # 資料位在第1筆
            break   # 資料位在第1筆
        
    icount += 1

try :
    saveFileDir = "產業分類\\"
    fileName = "產業分類" + ".htm"
    print('檔案名稱：' + fileName)
    with open(saveFileDir + fileName, 'w') as out :
        out.write(resp.text)

    print('資料儲存完成!!')
except IOError as err :
    print('Fie error : ' + str(err))

"""

rawtext=urlopen('http://www.ccnu.edu.cn',timeout=15).read();
print(rawtext)
rawtext=rawtext.decode('gbk')
print(rawtext)

"""
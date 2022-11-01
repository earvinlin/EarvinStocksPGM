"""

"""

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
    print("syntax : C:\python GetIndustryClassification.py 20170401 ")
    sys.exit()
"""

HYPER_LINK = "https://sjmain.esunsec.com.tw"
ssl._create_default_https_context = ssl._create_unverified_context
#
# 玉山證券：產業分析 -> 類股行情表
# https://www.esunsec.com.tw/tw-market/z/ze/zeg/zeg_23.djhtm
#
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

table = soup.find(lambda tag: tag.name=='table' and \
    tag.has_key('id') and tag['id']=="oMainTable")


rowCount = 0
serialCount = 0
blnFindTagA = False
for sibling in table.tr.next_siblings:
    print('處理筆數= ', str(rowCount))
    
    theTR = BeautifulSoup(repr(sibling), 'lxml')
    tds = theTR.findAll(lambda tag: tag.name=='td')
    print(len(tds), str(blnFindTagA), str(serialCount))
    for theTD in theTR.findAll(lambda tag: tag.name=='td') :
        for link in theTD.findAll('a') :
            print(str(rowCount), str(serialCount), link.get('href'), link.text)
            blnFindTagA = True

    print('-----', str(blnFindTagA))
    if blnFindTagA == True :
        serialCount += 1
        blnFindTagA = False
        print("In loop: ", str(blnFindTagA), str(serialCount))
        
    rowCount += 1
print("END!!! ", str(rowCount))



try :
#   下面這行有bug，會因為平台不同而有錯誤發生(要判斷執行程式的平台)    
    saveFileDir = "IndustryClassification\\"
    fileName = "IC" + ".htm"
    print('FileName：' + fileName)
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
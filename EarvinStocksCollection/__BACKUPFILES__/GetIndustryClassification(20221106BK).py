"""

python GetIndustryClassification.py IndustryClassification\ ic20221102.txt
"""

import re
import sys
import csv
import ssl
import requests
#import urllib.parse
#import urllib.request
from bs4 import BeautifulSoup


if len(sys.argv) < 3 :
    print("You need input two parameter(fmt : directory filename)")
    print("syntax : C:\python GetIndustryClassification.py IndustryClassification\\ ic20221102.txt ")
    sys.exit()


# for windows now (2022.11.02)
#saveFileDir = "IndustryClassification\\"
#fileName = "test.txt"
saveFileDir = sys.argv[1]
fileName = sys.argv[2]
outfile = open(saveFileDir + fileName, 'w')

#HYPER_LINK = "https://sjmain.esunsec.com.tw"
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




HYPER_LINK = "https://sjmain.esunsec.com.tw"
rowCount = 0
serialCount = 0
blnFindTagA = False
classType = ""
bln1stRecord = True

for sibling in table.tr.next_siblings:
    print('處理筆數= ', str(rowCount))
    
    theTR = BeautifulSoup(repr(sibling), 'lxml')
    tds = theTR.findAll(lambda tag: tag.name=='td')
    print(len(tds), str(blnFindTagA), str(serialCount))
    for theTD in theTR.findAll(lambda tag: tag.name=='td') :
        for link in theTD.findAll('a') :
            if bln1stRecord == True :
                classType = "M"
                bln1stRecord = False
            else :
                classType = "S"
            theAddr = HYPER_LINK + link.get('href')
            classCode = theAddr[(theAddr.find('a=')+2):]
#           產業分類(M大項_S子項)、產業分類代碼、網址、產業分類名稱
#            print(str(rowCount), str(serialCount), classType, classCode, theAddr, link.text)
            theInsertCmd = "insert into industry_classification (groupid, classificationType, classificationCode, " + \
                "classificationName, hrefAddr) values (" + str(serialCount) + ", '" + \
                classType + "', '" + classCode + "', '" + link.text + "', '" + theAddr + "');"
#            print(theInsertCmd)
            outfile.write(theInsertCmd + "\n")
            blnFindTagA = True

    print('-----')
    if blnFindTagA == True :
        serialCount += 1
        blnFindTagA = False
        bln1stRecord = True
        
    rowCount += 1
    
print("END!!! ", str(rowCount))
outfile.close()





"""
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



rawtext=urlopen('http://www.ccnu.edu.cn',timeout=15).read();
print(rawtext)
rawtext=rawtext.decode('gbk')
print(rawtext)

"""
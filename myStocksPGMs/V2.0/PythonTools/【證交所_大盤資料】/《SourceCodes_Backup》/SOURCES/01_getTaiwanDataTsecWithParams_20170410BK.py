import re
import sys
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

if len(sys.argv) < 3 :
    print("You need input two parameter(fmt : theProcessYear theProcessMonth)")
    print("syntax : C:\python 01_taiwanDataTSECDataWithParams.py 88 05 ")
    sys.exit()

params = urllib.parse.urlencode({'myear':sys.argv[1], 'mmon':sys.argv[2]}) #這是我自己的參數
params = params.encode('big5')
url = "http://www.tse.com.tw/ch/trading/indices/MI_5MINS_HIST/MI_5MINS_HIST.php"

f = urllib.request.urlopen(url, params)
bsObj = BeautifulSoup(f.read())
tableObj = bsObj.findAll("table")

try :
    # 取得資料的日期
    theTD = tableObj[7].find('td')
    theDate = theTD.get_text()
    theYMD = re.findall('[0-9]+', theDate)
    print('資料日期：' + theYMD[0] + theYMD[1])
    fileName = "大盤指數_" + theYMD[0] + theYMD[1] + ".txt"
    print('檔案名稱：' + fileName)

    with open(fileName, 'w') as out :
        # Table第1列內容為[91 年04月 發行量加權股價指數歷史資料]，略掉不寫入檔案
        omitFirstLine = True
        for theTR in tableObj[7].findAll('tr') :
            outputStr = ""
            if not omitFirstLine :
                for theTD in theTR.findAll('td') :
                    outputStr += theTD.get_text() + ";"
                if len(outputStr) > 1 :
                    out.write(outputStr + "\n")
            omitFirstLine = False

    print('資料處理完成!!')
except IOError as err :
    print('Fie error : ' + str(err))


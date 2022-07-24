import re
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

params = urllib.parse.urlencode({'myear':'88', 'mmon':'06'}) #這是我自己的參數
params = params.encode('big5') #這裡很重要，沒有encode會有error
url = "http://www.tse.com.tw/ch/trading/indices/MI_5MINS_HIST/MI_5MINS_HIST.php"

f = urllib.request.urlopen(url, params)

bsObj = BeautifulSoup(f.read())
tableObj = bsObj.findAll("table")

try :
    # 取得資料的日期
    theTD = tableObj[7].find('td')
    theDate = theTD.get_text().encode('latin1', 'ignore').decode('CP950')
    theYMD = re.findall('[0-9]+', theDate)
    print('資料日期：' + theYMD[0] + theYMD[1])
    fileName = "大盤指數_" + theYMD[0] + theYMD[1] + ".txt"

    with open(fileName, 'w') as out :
        omitFirstLine = True
        for theTR in tableObj[7].findAll('tr') :
            outputStr = ""
            if not omitFirstLine :
                for theTD in theTR.findAll('td') :
                    outputStr += theTD.get_text() + "#"
                if len(outputStr) > 1 :
                    out.write(outputStr.encode('CP950','ignore').decode('CP950','ignore') + "\n")
            omitFirstLine = False

    print('資料處理完成!!')
except IOError as err :
    print('Fie error : ' + str(err))


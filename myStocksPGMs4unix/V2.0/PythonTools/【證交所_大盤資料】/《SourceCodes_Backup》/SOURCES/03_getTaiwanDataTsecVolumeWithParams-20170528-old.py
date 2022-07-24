import re
import sys
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

if len(sys.argv) < 3 :
    print("You need input two parameter(fmt : theSelectYear(西元年，長度4位) theSelectMonth(月份，不足2位前面補0))")
    print("syntax : C:\python 03_getTaiwanDataTsecVolumeWithParams.py 2017 04 ")
    sys.exit()

params = urllib.parse.urlencode({'query_year':sys.argv[1], 'query_month':sys.argv[2]}) #這是我自己的參數
params = params.encode('big5')
url = "http://www.tse.com.tw/ch/trading/exchange/FMTQIK/FMTQIK.php"

f = urllib.request.urlopen(url, params)
bsObj = BeautifulSoup(f.read())
tableObj = bsObj.findAll("table")

try :
    # 取得資料的日期
    theTD = tableObj[0].find('td')
    theDate = theTD.get_text()
    theYMD = re.findall('[0-9]+', theDate)
    print('資料日期：' + theYMD[0] + theYMD[1])
    fileName = "大盤成交量_" + theYMD[0] + theYMD[1] + ".txt"
    print('檔案名稱：' + fileName)
    with open(fileName, 'w') as out :
        # Table第1列內容為[106年04月市場成交資訊  (元，股)]，略掉不寫入檔案
        omitFirstLine = True
        for theTR in tableObj[0].findAll('tr') :
            outputStr = ""
            if not omitFirstLine :
                for theTD in theTR.findAll('td') :
                    outputStr += theTD.get_text() + ";"
                if len(outputStr) > 1 :
                    out.write(outputStr.encode('CP950', 'ignore').decode('CP950') + "\n")
            else :
                omitFirstLine = False

    print('資料處理完成!!')
except IOError as err :
    print('Fie error : ' + str(err))


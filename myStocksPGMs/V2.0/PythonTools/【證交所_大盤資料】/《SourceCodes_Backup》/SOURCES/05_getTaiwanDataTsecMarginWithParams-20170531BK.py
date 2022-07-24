import re
import sys
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

if len(sys.argv) < 3 :
    print("You need input two parameter(fmt : yyyymmdd(西元日期) type(交易型態,值請檢視網頁原始檔))")
    print("syntax : C:\python 05_getTaiwanDataTsecMarginWithParams.py 20170405 MS ")
    sys.exit()

querydate = str(int(sys.argv[1][0:4])-1911) + "/" + sys.argv[1][4:6] + "/" + sys.argv[1][6:8]
selectType = sys.argv[2]

params = urllib.parse.urlencode({'qdate':querydate, 'selectType':selectType}) #這是我自己的參數
params = params.encode('big5')
url = "http://www.twse.com.tw/ch/trading/exchange/MI_MARGN/MI_MARGN.php"

f = urllib.request.urlopen(url, params)
bsObj = BeautifulSoup(f.read())
tableObj = bsObj.findAll("table")

try :
    # 取得資料的日期
    theTD = tableObj[0].find('td')
    theDate = theTD.get_text()
    theYMD = re.findall('[0-9]+', theDate)
    print('資料日期：' + theYMD[0] + theYMD[1])
    fileName = "大盤融資融券_" + theYMD[0] + theYMD[1] + theYMD[2] + ".txt"
    print('檔案名稱：' + fileName)
    with open(fileName, 'w') as out :
        # Table第1列內容為[105年04月14日 信用交易統計]，略掉不寫入檔案
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


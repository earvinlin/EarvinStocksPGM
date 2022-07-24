import re
import sys
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

#params = urllib.parse.urlencode({'myear':sys.argv[1], 'mmon':sys.argv[2]}) #這是我自己的參數
#params = params.encode('big5')


if len(sys.argv) < 2 :
    print("You need input one parameter(fmt : theProcessDate(yyyy/mm/dd))")
    print("syntax : C:\python 01_taiwanDataTSECDataWithParams.py 106/02/06 ")
    sys.exit()

print("input-value= " + sys.argv[1] + "\n")
#params = urllib.parse.urlencode({"input_date": "106/02/06"}) #這是我自己的參數
params = urllib.parse.urlencode({"qdate": sys.argv[1]}) #這是我自己的參數
params = params.encode('big5') #這裡很重要，沒有encode會有error
url = "http://www.tse.com.tw/ch/trading/exchange/BWIBBU/BWIBBU_d.php"
f = urllib.request.urlopen(url, params)
#print(f.read())

bsObj = BeautifulSoup(f.read())

try :
    # 取得資料的日期
    tableObj = bsObj.find_all("table")
    theTD = tableObj[0].find('td')
    theDate = theTD.get_text()
    theYMD = re.findall('[0-9]+', theDate)
    print('資料日期：' + theYMD[0] + theYMD[1] + theYMD[2])
    fileName = "stocks_個股日本益比殖利率及股價淨值比-" + theYMD[0] + theYMD[1] + theYMD[2] + ".txt"

    with open(fileName, 'w') as out :
        # 取得標頭列
        omitFirstLine = True
        theThead = bsObj.find_all("thead")
        for theTR in theThead[0].find_all('tr') :
            print("In thead= " + str(theThead))
            outputStr = ""
            if not omitFirstLine :
                for theTD in theTR.find_all('td') :
                    outputStr += theTD.get_text() + ";"
                print("In thead = " + outputStr)
                if len(outputStr) > 1 :
                    out.write(outputStr.encode('CP950', 'ignore').decode('CP950') + "\n")
            omitFirstLine = False

        # 取得表格內容
        theTBody = bsObj.find_all("tbody")
        for theTR in theTBody[0].find_all('tr') :
            outputStr = ""
            for theTD in theTR.find_all('td') :
                outputStr += theTD.get_text() + ";"
            if len(outputStr) > 1 :
                out.write(outputStr.encode('CP950', 'ignore').decode('CP950') + "\n")

    print('資料處理完成!!')
except IOError as err :
    print('Fie error : ' + str(err))


import re
from urllib.request import urlopen
from bs4 import BeautifulSoup


# 20170115 Not Finished!!!!!!!!!!!!!!!!!!!
'''
request = urllib2.Request("http://www.tse.com.tw/ch/trading/exchange/BWIBBU/BWIBBU_d.php") 

request.add_header("User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36")
form_data = {
    "StartStation": "977abb69-413a-4ccf-a109-0272c24fd490", 
    "EndStation": "f2519629-5973-4d08-913b-479cce78a356",
    "SearchDate": "2016/01/10",
    "SearchTime": "17:00",
    "SearchWay":"DepartureInMandarin",
    "RestTime":"",
    "EarlyOrLater":""
}
form_data = urllib.urlencode(form_data)
response = urllib2.urlopen(request,data=form_data)  

bsObj = BeautifulSoup(response.read())
tableObj = bsObj.findAll("table")
'''
# --------------------------------------------------------------------------------------

html = urlopen("http://www.tse.com.tw/ch/trading/exchange/BWIBBU/BWIBBU_d.php")
bsObj = BeautifulSoup(html.read())
tableObj = bsObj.findAll("table")

try :
    # 取得資料的日期
    theTH = tableObj[7].find('th')
    theDate = theTH.get_text().encode('latin1', 'ignore').decode('CP950')
    theYMD = re.findall('[0-9]+', theDate)
    print('資料日期：' + theYMD[0] + theYMD[1] + theYMD[2]) 
    fileName = "stocks_個股日本益比殖利率及股價淨值比-" + theYMD[0] + theYMD[1] + theYMD[2] + ".txt"
    
    with open(fileName, 'w') as out :        
        for theTR in tableObj[7].findAll('tr') :
            outputStr = ""
            for theTD in theTR.findAll('td') :
                outputStr += theTD.get_text() + ","        
#            print(outputStr.encode('latin1', 'ignore').decode('CP950'))
            if len(outputStr) > 1 :
                out.write(outputStr.encode('latin1', 'ignore').decode('CP950') + "\n")

    print('資料處理完成!!') 
except IOError as err :
    print('Fie error : ' + str(err))

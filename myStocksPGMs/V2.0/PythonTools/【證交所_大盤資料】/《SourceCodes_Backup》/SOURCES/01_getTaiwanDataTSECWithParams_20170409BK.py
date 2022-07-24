import re
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

params = urllib.parse.urlencode({'myear':'88', 'mmon':'06'}) #�o�O�ڦۤv���Ѽ�
params = params.encode('big5') #�o�̫ܭ��n�A�S��encode�|��error
url = "http://www.tse.com.tw/ch/trading/indices/MI_5MINS_HIST/MI_5MINS_HIST.php"

f = urllib.request.urlopen(url, params)

bsObj = BeautifulSoup(f.read())
tableObj = bsObj.findAll("table")

try :
    # ���o��ƪ����
    theTD = tableObj[7].find('td')
    theDate = theTD.get_text().encode('latin1', 'ignore').decode('CP950')
    theYMD = re.findall('[0-9]+', theDate)
    print('��Ƥ���G' + theYMD[0] + theYMD[1])
    fileName = "�j�L����_" + theYMD[0] + theYMD[1] + ".txt"

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

    print('��ƳB�z����!!')
except IOError as err :
    print('Fie error : ' + str(err))


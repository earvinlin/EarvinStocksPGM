import re
import sys
import shutil

if len(sys.argv) < 2 :
    print("You need input one parameter(fmt : theProcessDate(yyyymmdd))")
    print("syntax : C:\python 01_getStocksDailyRatiosData.py 20170501 ")
    sys.exit()

print("input-value= " + sys.argv[1] + "\n")

try :
    data = []   # 儲存要寫出的檔案內容
    saveFileDir = "Files/"
    fileName = "stocks_個股日本益比殖利率及股價淨值比-" + sys.argv[1] + ".txt"
    bk_fileName = "BK_" + fileName   # 先把原始檔案備份一份

    shutil.copy(saveFileDir + fileName, saveFileDir + bk_fileName)
    infile = open(saveFileDir + bk_fileName, 'r')
    for line in infile.readlines():
        data.append(line)
    infile.close()

    i = 0
    outfile = open(saveFileDir + fileName, 'w')
    while i < len(data):
        if len(re.findall("^\"\d{4}", data[i])) or len(re.findall("^\"證券代號", data[i])) > 0:
            outfile.write(data[i])
        i += 1

    print('資料儲存完成!!')
    outfile.close()
except IOError as err :
    print('Fie error : ' + str(err))


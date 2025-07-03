import re
import sys
import shutil

if len(sys.argv) < 2 :
    print("You need input two parameter(fmt : theDate(yyyymmdd))")
    print("syntax : C:\python 03_formatTaiwanDataTsecVolumeWithParams2.py 20170401 ")
    sys.exit()

try :
    data = []   # 儲存要寫出的檔案內容
# 20250702 判斷程式是在何種作業系統執行以確認路徑撰寫方式
#    saveFileDir = "大盤成交量\\"
    saveFileDir = ""
    if sys.platform == "darwin" or sys.platform == "linux" :
        saveFileDir = "大盤成交量/"
    else :
        saveFileDir = "大盤成交量\\"
# 20250702 --- END ---

    fileName = "大盤成交量_" + sys.argv[1] + ".txt"
    bk_fileName = "BK_" + fileName   # 先把原始檔案備份一份

    shutil.copy(saveFileDir + fileName, saveFileDir + bk_fileName)
    infile = open(saveFileDir + bk_fileName, 'r')
    for line in infile.readlines():
        data.append(line)
    infile.close()

    i = 0
    outfile = open(saveFileDir + fileName, 'w')
    while i < len(data):
        if len(re.findall("\d{3}\/\d{2}\/\d{2}", data[i])) or len(re.findall("成交股數", data[i])) > 0:
            outfile.write(data[i])
        i += 1

    print('資料儲存完成!!')
    outfile.close()
except IOError as err :
    print('Fie error : ' + str(err))

import re
import sys
import shutil

if len(sys.argv) < 2 :
    print("You need input two parameter(fmt : yyyymmdd(西元日期) type(交易型態,值請檢視網頁原始檔))")
    print("syntax : C:\python FormatTaiwanDataPolarisWithParams_V1.1.py 20170405 ")
    sys.exit()

try :
    data = []   # 儲存要寫出的檔案內容

# 20250704 判斷程式是在何種作業系統執行以確認路徑撰寫方式
#    saveFileDir = "Files\\"
    saveFileDir = ""
    if sys.platform == "darwin" or sys.platform == "linux" :
        saveFileDir = "Files/"
    else :
        saveFileDir = "Files\\"
# 20250704 --- END ---

    insertCnt = 0
    theFileName = sys.argv[1]
    input_file = theFileName + ".TXT"
    theTradeDate = int(int(theFileName[5:9])-1911)*10000 + int(theFileName[9:11])*100 + int(theFileName[11:])
    print("The trade date is " + str(theTradeDate))
    bk_input_file = "BK_" + input_file   # 先把原始檔案備份一份
    
    shutil.copy(saveFileDir + input_file, saveFileDir + bk_input_file)
    infile = open(saveFileDir + bk_input_file, 'r')
    
    for line in infile.readlines():
        data.append(line)
    infile.close()

    readCount = 0
# 20250704 判斷程式是在何種作業系統執行以確認編碼，方能正確讀取檔案

#    outfile = open(saveFileDir + input_file, 'w')
    stocks = open(saveFileDir + input_file, 'w', encoding="cp950")
# 20250704 --- END ---

    while readCount < len(data):
        if len(re.findall("^[0-9]{4}", data[readCount])) or len(re.findall("^[a-zA-Z][a-zA-Z0-9]", data[readCount])) > 0:

            if re.search("MSCI A", data[readCount]):
                print("Readline " + str(readCount) + ": \"MSIC A\" found!!")
                subData = re.sub("MSCI A", "MSCI_A", data[readCount], 1)
                outfile.write(subData)
            elif re.search("新光Shiller CAPE", data[readCount]):
                print("Readline " + str(readCount) + ": \"新光Shiller CAPE\" found!!")
                subData = re.sub("新光Shiller CAPE", "新光Shiller_CAPE", data[readCount], 1)
                outfile.write(subData)           
            elif re.search("0▲", data[readCount]):
                print("Readline " + str(readCount) + ": \"0▲\" found!!")
                subData = re.sub("0▲", "0 ▲", data[readCount], 1)
                outfile.write(subData)           
            elif re.search("0▼", data[readCount]):
                print("Readline " + str(readCount) + ": \"0▼\" found!! data=" + data[readCount][0:20])
                subData = re.sub("0▼", "0 ▼", data[readCount], 1)
                outfile.write(subData)           
            elif re.search("凱基ESG BBB債15+", data[readCount]):
                print("Readline " + str(readCount) + ": \"凱基ESG BBB債15+\" found!!")
                subData = re.sub("凱基ESG BBB債15+", "凱基ESG_BBB債15+", data[readCount], 1)
                outfile.write(subData)           
            else:
                outfile.write(data[readCount])
        else:
            print("omit rec: " + data[readCount]) # Display不會寫檔的資料於畫面上確認
        readCount += 1

    print('資料儲存完成!!')
    outfile.close()
except IOError as err :
    print('Fie error : ' + str(err))

'''
<20220723 Created>
本版本主要是修改為可在Linux / iMac上執行的版本
但是，在路徑取得方面Linux / iMac找不到簡單的做法，是待解決的事項
Winodws exec. example      : 
    python 02_insertTaiwanDataTsecToMySQLDB_V2.py 20220701
Linux / iMac exec. example : 
    python3 02_insertTaiwanDataTsecToMySQLDB_V2.py 20220701
'''
import mysql.connector
import datetime
import sys
import os
import csv
import platform

user = 'root'
pwd  = 'lin32ledi'
host = '127.0.0.1'
db   = 'stocksdb'

# 檔案名程格式：大盤融資融券_yyymmdd.txt
# 資料來自證交所網站，包含下列欄位：項目, 買進, 賣出, 現金(券)償還, 前日餘額, 今日餘額
select_sql = "SELECT * FROM taiwan_data_tsec_margin where date = %s and type = %s "

cnx = mysql.connector.connect(user=user, password=pwd, host=host, database=db)
cursor = cnx.cursor()

try:
    if len(sys.argv) < 1 :
        print("You need input one parameter(fmt : yyymmdd (民國日期))")
        print("syntax : C:\python 06_insertTaiwanDataTsecMarginToMySQLDB.py 1060414 ")
        sys.exit()

#    saveFileDir = "大盤融資融券\\"
#    tsec = open(input_file, 'r', encoding = 'UTF-8') # 以utf-8開啟
#    tsec = open(saveFileDir + input_file, 'r')	# 預設以系統編碼開啟
    input_file = "大盤融資融券_" + sys.argv[1] + ".txt"
    print(input_file)
    saveFileDir = ""
    if platform.system() == "Windows" :
        saveFileDir = "大盤融資融券\\"
        tsec = open(saveFileDir + input_file, 'r')	# 預設以系統編碼開啟
    elif platform.system() == "Linux" :
#       Linux 如何取得程式執行路徑 ?? -- 20220723 Wait to solve ...        
        saveFileDir = "/home/earvin/Dropbox/myStocksPGMs/V2.0/PythonTools/【證交所_大盤資料】/大盤融資融券/"
        tsec = open(saveFileDir + input_file, 'r', encoding = 'cp950')	# 預設以系統編碼開啟
    else :
#       iMac 如何取得程式執行路徑 ?? -- 20220723 Wait to solve ...        
        saveFileDir = "/Users/earvin/workspaces/GithubProjects/EarvinStocksPGM/myStocksPGMs4unix/V2.0/PythonTools/【證交所_大盤資料】/大盤融資融券/"

        tsec = open(saveFileDir + input_file, 'r', encoding = 'cp950')	# 預設以系統編碼開啟

    reader = csv.DictReader(tsec, delimiter=',')

#	NOTE : parse 日期 yyy/mm/dd (因為民國年可能為2位數或3位數，所以改由後面算長度)
    theDate = sys.argv[1][0:4] + "/" + sys.argv[1][4:6] + "/" + sys.argv[1][6:]
    print("交易日期= " + theDate)
    tehDateList = theDate.split("/")
    theTradeDate = datetime.date((int(tehDateList[0])), int(tehDateList[1]), int(tehDateList[2]))  # 轉西元日期

    insertCnt = 0
    for row in reader :
        theType = "3"
        if row['項目'] == "融資(交易單位)" :
            theType = "1"
        elif row['項目'] == "融券(交易單位)" :
            theType = "2"

#       先查資料是否已存在，存在要用更新；不存在用新增!!
        cursor.execute(select_sql, (theTradeDate, theType))
        data = cursor.fetchall()

        if not data :
#           insert data to db
#           買進;賣出;現金(券)償還;前日餘額;今日餘額;
            theBuy = float(row['買進'].replace(',', ''))
            theSell = float(row['賣出'].replace(',', ''))
            theReturn = float(row['現金(券)償還'].replace(',', ''))
            theYes_balance = float(row['前日餘額'].replace(',', ''))
            theBalance = float(row['今日餘額'].replace(',', ''))
            insertstmt=("INSERT INTO taiwan_data_tsec_margin (`date`, `type`, `buy`, `sell`, `return`, `yes_balance`, `balance`) VALUES ('%s', '%s', '%f', '%f', '%f', '%f', '%f')" % (theTradeDate, theType, theBuy, theSell, theReturn, theYes_balance, theBalance))
            cursor.execute(insertstmt)
            insertCnt += 1
        else :
            print("Duplicate data, the trade_date = " + str(theTradeDate) + ", the type = " + theType);

except mysql.connector.Error as err:
    print("insert to table 'taiwan_data_tsec_margin' failed.")
    print("Error: {}".format(err.msg))
    sys.exit()

print("新增資料完成!! 共 " + str(insertCnt) + " 筆。")
tsec.close()
cnx.commit()
cursor.close()
cnx.close()

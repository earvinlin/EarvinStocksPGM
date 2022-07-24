import mysql.connector
import datetime
import sys
import os
import csv

user = 'root'
pwd  = 'lin32ledi'
host = '127.0.0.1'
db   = 'stocksdb'

# 檔案名程格式：大盤指數_yymm.txt
# 資料來自證交所網站，包含下列欄位：日期, 開盤指數, 最高指數, 最低指數, 收盤指數
select_sql = "SELECT * FROM taiwan_data_tsec where date = %s"

cnx = mysql.connector.connect(user=user, password=pwd, host=host, database=db)
cursor = cnx.cursor()

try:
    if len(sys.argv) < 2 :
        print("You need input one parameter(fmt : theDate(yyyymmdd))")
        print("syntax : C:\python 02_insertTaiwanDataTsecToMySQLDB.py 20170501 ")
        sys.exit()

    saveFileDir = "大盤指數\\"
    input_file = "大盤指數_" + sys.argv[1] + ".txt"
    print(input_file)
    csvHeader = []

    tsec = open(saveFileDir + input_file, 'r')	# 預設以系統編碼開啟
	omit = 0
    for line in tsec:
        print(line)
        omit += 1
        if omit == 2:
            csvHeader = line

        	


except mysql.connector.Error as err:
    print("insert to table 'taiwan_data_tsec' failed.")
    print("Error: {}".format(err.msg))
    sys.exit()

print("新增資料完成!! 共 " + str(insertCnt) + " 筆。")
tsec.close()
cnx.commit()
cursor.close()
cnx.close()

import mysql.connector
import sys
import os
import csv

user = 'root'
pwd  = 'lin32ledi'
host = '127.0.0.1'
db   = 'stocksdb'

select_sql = "SELECT * FROM taiwan_data_stocks_daily_ratios where stock_no = %s and date = %s"


input_file = 'stocks.txt'

cnx = mysql.connector.connect(user=user, password=pwd, host=host, database=db)
cursor = cnx.cursor()

try:
#    cursor.execute(create_table_sql)
    insertCnt = 0
    theDate = int(sys.argv[1])
    thePERatio = 0.0
    theYields = 0.0
    thePBratio = 0.0
# 沒有輸入檔名的話，預設是處理stocks.txt
    if len(sys.argv) > 2 :
    	input_file = sys.argv[2]

#    saveFileDir = "Files\\BACKUP_FILES\\重抓一次資料(StartWith950902)\\"
# 20250702 判斷程式是在何種作業系統執行以確認路徑撰寫方式
#    saveFileDir = "Files\\"
    saveFileDir = ""
    if sys.platform == "darwin" or sys.platform == "linux" :
        saveFileDir = "Files//"
    else :
        saveFileDir = "Files\\"
# 20250702 --- END ---

# 20221012 來源資料若是從unix抓下來，檔案編碼會是utf8，在windows上跑要加上「encoding="utf8"」解碼
#    stocks = open(saveFileDir + input_file, 'r', encoding="utf8")
# 20250702 判斷程式是在何種作業系統執行以確認編碼，方能正確讀取檔案
    theEncoding = ""
    if sys.platform == "darwin" or sys.platform == "linux" :
        theEncoding = "utf-8"
    else :
        theEncoding = "cp950"
#    stocks = open(saveFileDir + input_file, 'r', encoding="cp950")
    stocks = open(saveFileDir + input_file, 'r', encoding=theEncoding)
# 20250702 --- END ---

    reader = csv.DictReader(stocks, delimiter=',')
    for row in reader :
        print(row)
        if row['本益比'] == '-' :
        	thePERatio = 0
        else :
        	thePERatio = float(row['本益比'].replace(",", ""))
        if row['殖利率(%)'] == '-' :
        	theYields = 0
        else :
        	theYields = float(row['殖利率(%)'].replace(",", ""))
        if row['股價淨值比'] == '-' :
        	thePBratio = 0
        else :
        	thePBratio = float(row['股價淨值比'].replace(",", ""))

# 0611  先查資料是否已存在，存在要用更新；不存在用新增!!
        cursor.execute(select_sql, (row['證券代號'], theDate))
        data = cursor.fetchall()

        if not data :
#           insert data to db
            insertstmt=("INSERT INTO taiwan_data_stocks_daily_ratios (date, stock_no, stock_name, pe_ratio, yields, pb_ratio) VALUES ('%d', '%s', '%s', '%f', '%f', '%f')" % (theDate, row['證券代號'], row['證券名稱'], thePERatio, theYields, thePBratio))
            cursor.execute(insertstmt)
            insertCnt += 1
        else :
        	print("Duplicate data, the trade_date = " + str(theDate) + ", the stock_no = " + row['證券代號']);

except mysql.connector.Error as err:
    print("insert record 'taiwan_data_stocks_daily_ratios' failed.")
    print("Error: {}".format(err.msg))
    sys.exit()

print("新增資料完成!! 共 " + str(insertCnt) + " 筆。")
stocks.close()
cnx.commit()
cursor.close()
cnx.close()

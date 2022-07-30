from base64 import decode
import mysql.connector
import sys
import os
import csv
import platform

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

    saveFileDir = ""
    if platform.system() == "Windows" :
        saveFileDir = "Files\\"
    elif platform.system() == "Linux" :
#       Linux 如何取得程式執行路徑 ?? -- 20220723 Wait to solve ...        
        saveFileDir = "/home/earvin/Dropbox/myStocksPGMs/V2.0/PythonTools/【新增寶來個股資料】/Files/"
    else :
#       iMac(放在公司的iMac路徑)如何取得程式執行路徑 ?? -- 20220723 Wait to solve ...     
        saveFileDir = "/Users/earvin/workspaces/GithubProjects/EarvinStocksPGM/myStocksPGMs4unix/V2.0/PythonTools/【新增個股3項財務指標】/Files/"

    stocks = open(saveFileDir + input_file, 'r', encoding = 'CP950')
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

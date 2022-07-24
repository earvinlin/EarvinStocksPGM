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
    tsec = open(saveFileDir + input_file, 'r')	# 預設以系統編碼開啟
    reader = csv.DictReader(tsec, delimiter=',')
	
    THE_STOCK_NO = 'taiex'
    THE_STOCK_NAME ='大盤指數'

    insertCnt = 0
    for row in reader :
#       先查資料是否已存在，存在要用更新；不存在用新增!!
#		NOTE : parse 日期 yy/mm/dd
        tehDateList = row['日期'].split('/')
        theDate = str(int(tehDateList[0])+1911) + "/" + str(tehDateList[1]) + "/" + str(tehDateList[2])
        print("交易日期= " + theDate)
        theTradeDate = datetime.date((int(tehDateList[0])+1911), int(tehDateList[1]), int(tehDateList[2]))
        cursor.execute(select_sql, (theTradeDate,))
        data = cursor.fetchall()

        if not data :
#           insert data to db
            theStartPrice = float(row['開盤指數'].replace(',', ''))
            theHighPrice = float(row['最高指數'].replace(',', ''))
            theLowPrice = float(row['最低指數'].replace(',', ''))
            theEndPrice = float(row['收盤指數'].replace(',', ''))
            insertstmt=("INSERT INTO taiwan_data_tsec (stock_no, date, stock_name, start_price, high_price, low_price, end_price) VALUES ('%s', '%s', '%s', '%f', '%f', '%f', '%f')" % (THE_STOCK_NO, theTradeDate, THE_STOCK_NAME, theStartPrice, theHighPrice, theLowPrice, theEndPrice))
            cursor.execute(insertstmt)
            insertCnt += 1
        else :
            print("Duplicate data, stock_no = " + THE_STOCK_NO + ", date = " + str(theTradeDate));

except mysql.connector.Error as err:
    print("insert to table 'taiwan_data_tsec' failed.")
    print("Error: {}".format(err.msg))
    sys.exit()

print("新增資料完成!! 共 " + str(insertCnt) + " 筆。")
tsec.close()
cnx.commit()
cursor.close()
cnx.close()

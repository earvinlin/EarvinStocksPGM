import mysql.connector
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
        print("You need input one parameter(fmt : theProcessYear theProcessMonth)")
        print("syntax : C:\python 02_insertTaiwanDataTsecToMySQLDB.py 88 05 ")
        sys.exit()

    input_file = "大盤指數_" + sys.argv[1] + sys.argv[2] + ".txt"
    print(input_file)
    tsec = open(input_file, 'r', encoding = 'UTF-8')
    reader = csv.DictReader(tsec, delimiter=';')
    insertCnt = 0
    for row in reader :
#        print(row)
#       先查資料是否已存在，存在要用更新；不存在用新增!!
#		日期要特別處理
#        theDate = int(row['日期'])
        print(row['日期'] + "," + str(row['開盤指數']) + "\n")

# 2017/04/09 parse 日期 yy/mm/dd
#            python新增資料欄位為data型態要如何新增？
#        tehDateList = row['日期'].split('/')
#        theDate = int(int(tehDateList[0])-1911)*10000 + int(tehDateList[1])*100 + int(tehDateList[2])
#        cursor.execute(select_sql, (theStockNo, theDate))
#        data = cursor.fetchall()

#        if not data :
#           insert data to db
#            insertstmt=("INSERT INTO taiwan_data_tsec (stock_no, date, start_price, high_price, low_price, end_price, volume, margin_trading, short_selling) VALUES ('%s', '%d', '%f', '%f', '%f', '%f', '%f', '%f', '%f')" % (theStockNo, theDate, float(row['開盤']), float(row['最高']), float(row['最低']), float(row['收盤']), float(row['成交量']), float(row['融資張數']), float(row['融券張數'])))
#            cursor.execute(insertstmt)
#            insertCnt += 1
#        else :
#            print("Duplicate data, stock_no = " + theStockNo + ", date = " + str(theDate));

except mysql.connector.Error as err:
    print("insert to table 'taiwan_data_stocks_7indexes' failed.")
    print("Error: {}".format(err.msg))
    sys.exit()

print("新增資料完成!! 共 " + str(insertCnt) + " 筆。")
tsec.close()
cnx.commit()
cursor.close()
cnx.close()

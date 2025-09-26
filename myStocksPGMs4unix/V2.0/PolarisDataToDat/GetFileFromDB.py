"""
傳入的參數為要處理的股票代號
產出的檔案名稱為股票代號(沒有副檔案)
"""


import mysql.connector
import sys
import os 
import csv
import time
 
user = 'root'
pwd  = 'lin32ledi'
host = '127.0.0.1'
db   = 'stocksdb'
 
select_sql = "SELECT DATE, START_PRICE, HIGH_PRICE, LOW_PRICE, END_PRICE, VOLUME, MARGIN_TRADING, SHORT_SELLING FROM TAIWAN_DATA_POLARIS_STOCKS WHERE STOCK_NO = %s ORDER BY DATE "
 
cnx = mysql.connector.connect(user=user, password=pwd, host=host, database=db)
cursor = cnx.cursor()
 
try:
	print("[GetFileFromDB.py] 開始執行時間：" + time.strftime('%Y-%m-%d   %H:%M:%S',time.localtime()))

	if len(sys.argv) < 2 :
		print("You need input one parameter(fmt : theStockNo)")
		print("syntax : C:\python GetFileFromDB.py 2002")
		sys.exit()

	loadFileDir = "csv\\"

	theStockNo = sys.argv[1]
	stocks = open(loadFileDir + sys.argv[1] + ".csv", 'w')
	insertCnt = 0
	cursor.execute(select_sql, (theStockNo, ))
	for row in cursor:
		outStr = ""
		for i in range(len(row)) :
			outStr += str(row[i]) + ","
		print(outStr[0:len(outStr)-1]) 
		stocks.write(outStr[0:len(outStr)-1] + "\n")
		insertCnt += 1

except mysql.connector.Error as err:
	print("insert to table 'taiwan_data_polaris_stocks' failed.")
	print("Error: {}".format(err.msg))
	sys.exit()

print("資料產生完成!! 共 " + str(insertCnt) + " 筆。")
stocks.close()
cursor.close()
cnx.close()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        

print("[GetFileFromDB.py] 結束執行時間：" + time.strftime('%Y-%m-%d   %H:%M:%S',time.localtime()))

"""
EarvinStocksAnalysis.GetPotentialStocks2 的 Docstring
Copy from GetPotentialStocks.py
用來找出潛力股 : 5個交易日內上漲10%以上的股票
CMD: python GetPotentialStocks2.py
SQL-CMD :
select date, stock_no, stock_name, start_price, high_price, low_price, end_price, volume 
from taiwan_data_polaris 
where stock_no = '1101' order by date;
"""
from pickle import FALSE
from xmlrpc.client import boolean
import mysql.connector
import datetime
import sys
import os
import csv
import numpy as np
import pandas as pd
import platform

user = 'root'
pwd  = 'lin32ledi'
host = '127.0.0.1'
db   = 'stocksdb'

# 絕對路徑：OK
#IMAC_PATH = "/Users/earvin/workspaces/GithubProjects/EarvinStocksPGM/EarvinStocksAnalysis/DATA/"
# 相對路徑：預設為Windows Platform
# 20250707 依不同平台撰寫路街格式
#DATA_PATH = "DATA\\POTENTIAL\\"
DATA_PATH = ""
if sys.platform == "darwin" or sys.platform == "linux" :
    DATA_PATH = "DATA/POTENTIAL/"
else :
    DATA_PATH = "DATA\\POTENTIAL\\"

# 打算比對的次數
DEF_COMP_TIME = 5

# 20250707 DEBUG
#input_file = "STOCKS_LIST.txt"
input_file = "STOCKS_LIST_test.txt"
output_file = "POTIENTIAL_STOCKS_LIST.txt"
readCnt = 0

cnx = mysql.connector.connect(user=user, password=pwd, host=host, database=db)
cursor = cnx.cursor()

try:
#    if len(sys.argv) < 2 :
#        print("You need input one parameter(fmt : theDate(yyyymmdd))")
#        print("syntax : C:\python 02_insertTaiwanDataTsecToMySQLDB.py 20250701 ")
#        sys.exit()

	theSQLCmd = "select date, stock_no, stock_name, start_price, " + \
				"high_price, low_price, end_price, volume " + \
				"from taiwan_data_polaris " + \
				"where stock_no = %s order by date;"


	print(input_file)
	twStocksList = open(input_file, 'r')	# 預設以系統編碼開啟
	stocks = twStocksList.readlines()
	for stockNo in stocks :
		stockNo = stockNo.replace('\n','')	# 不知為何檔案會有換行符號
		print("正在處理", stockNo)
		theArgs = (stockNo,)
		print("正在處理股票代號：", theArgs)
#       <20250708 wait to confirm>判斷每年盈收成長率是否大於10%(連續3年)
		print(theSQLCmd)
		cursor.execute(theSQLCmd, theArgs)
		data = cursor.fetchall()
		
		if not data :
			print("No data found!!!")
		else :
			df = pd.DataFrame(data, columns=['日期','股票代號', '股票名稱', '開盤價', \
				'最高價', '最低價', '收盤價', '成交量'])		

			print(data)


		readCnt += 1

except mysql.connector.Error as err:
    print("Processing Error!!! ")
    print("Error: {}".format(err.msg))
    sys.exit()

print("資料處理完成!! 共 " + str(readCnt) + " 筆。")
twStocksList.close()
cnx.commit()
cursor.close()
cnx.close()

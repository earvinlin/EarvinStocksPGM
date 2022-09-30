"""
取得在n年內股價漲n倍的股票

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
DATA_PATH = "DATA\\MYNT\\"

# 打算比對的次數
DEF_COMP_TIME = 8

input_file = "STOCKS_LIST_test.txt"
output_file = "M_YEAR_N_TIMES_STOCKS_LIST.txt"
readCnt = 0

cnx = mysql.connector.connect(user=user, password=pwd, host=host, database=db)
cursor = cnx.cursor()

if len(sys.argv) < 3 :
    print("You need input two parameter(fmt : M_year N_times)")
    print("syntax : C:\python GetStocksInMYearNTimes.py 2 4 ## 表示尋找2年內上漲4倍以上的股票 ")
    sys.exit()

try :
#	select stock_no, dividend_year, stock_price_year, year_high_price, year_low_price from stocks_dividend where stock_no = '2049' order by stock_price_year, dividend_year;
	theSQLCmd = "select stock_no, dividend_year, stock_price_year, " + \
				"year_high_price, year_low_price from stocks_dividend " + \
				"where stock_no = %s order by stock_price_year, dividend_year "

	print(input_file)
	twStocksList = open(input_file, 'r')	# 預設以系統編碼開啟
	stocks = twStocksList.readlines()
	for stockNo in stocks :
		stockNo = stockNo.replace('\n','')	# 不知為何檔案會有換行符號
		print("正在處理", stockNo)
		theArgs = (stockNo,)
#       判斷每年盈收成長率是否大於10%(連續3年)
		cursor.execute(theSQLCmd, theArgs)
		data = cursor.fetchall()
		
		if not data :
			print("No data found!!!")
		else :
			print("Get it!!!")
			df = pd.DataFrame(data, columns=['股票代號','股利發放年度', \
				'股價年度','年度股價最高價','年度股價最低價'])	
#			print(df)
				

		readCnt += 1

except mysql.connector.Error as err:
	print("Processing Error!!! ")
	print("Error: {}".format(err.msg))
	sys.exit()

print("資料處理完成!! 共 " + str(readCnt) + " 筆。")

cnx.commit()
cursor.close()
cnx.close()

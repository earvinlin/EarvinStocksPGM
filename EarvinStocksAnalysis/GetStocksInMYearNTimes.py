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
#	注意，有些個股有季配，所以資料會有重複，因此加上「year_high_price is not null」條件過濾
#	select stock_no, dividend_year, stock_price_year, year_high_price, year_low_price from stocks_dividend where year_high_price is not null and stock_no = '2049' order by stock_price_year, dividend_year;
	theSQLCmd = "select stock_no, dividend_year, stock_price_year, " + \
				"year_high_price, year_low_price from stocks_dividend " + \
				"where year_high_price is not null and " + \
				"stock_no = %s order by stock_price_year, dividend_year "

	print(input_file)
	twStocksList = open(input_file, 'r')	# 預設以系統編碼開啟
	stocks = twStocksList.readlines()
	for stockNo in stocks :
		stockNo = stockNo.replace('\n', '')	# 不知為何檔案會有換行符號
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
			df['p0'] = None
			df['p1'] = None
			df['p2'] = None
			print(df)
			print("df counts: ",len(df))
			counts = len(df)
			
			for i in range(counts) :
				print(i)
				if df.at[i,'年度股價最低價'] is None :
					print(df.at[i,'年度股價最低價'])
					continue
				lowPrice = df.at[i,'年度股價最低價']
				highPrice = df.at[i,'年度股價最高價']
				diff00 = (highPrice - lowPrice) / lowPrice
				df.iloc[i,5] = "{:.2f}".format(diff00)
#				次年				
				if i < (counts - 1) :
					highPrice1st = df.at[i + 1,'年度股價最高價']
					diff01 = (highPrice1st - lowPrice) / lowPrice
					df.iloc[i,6] = "{:.2f}".format(diff01)
#				2年
				if i < (counts - 2) :
					highPrice2nd = df.at[i + 2,'年度股價最高價']
					diff02 = (highPrice2nd - lowPrice) / lowPrice
					df.iloc[i,7] = "{:.2f}".format(diff02)
			print(df)
			df.to_csv("test.csv", encoding='cp950')

		readCnt += 1

except mysql.connector.Error as err:
	print("Processing Error!!! ")
	print("Error: {}".format(err.msg))
	sys.exit()

print("資料處理完成!! 共 " + str(readCnt) + " 筆。")

cnx.commit()
cursor.close()
cnx.close()
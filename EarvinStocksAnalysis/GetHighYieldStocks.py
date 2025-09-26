"""
取得高殖利率股票 
syntax : GetHighYieldStocks.py yield-rate(fmt: 0.04)
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
#DATA_PATH = "DATA\\"
DATA_PATH = "TEST\\"  # 20240519 程式測試中…

# 打算比對的次數
DEF_COMP_TIME = 8

input_file = "STOCKS_LIST.txt"
output_file = "POTIENTIAL_STOCKS_LIST.txt"
readCnt = 0

cnx = mysql.connector.connect(user=user, password=pwd, host=host, database=db)
cursor = cnx.cursor()

try:
#    if len(sys.argv) < 2 :
#        print("You need input one parameter(fmt : theDate(yyyymmdd))")
#        print("syntax : C:\python 02_insertTaiwanDataTsecToMySQLDB.py 20170501 ")
#        sys.exit()

	theSQLCmd = "select a.股票代號, d.stock_name as 股票名稱, a.年度, a.累計營收_億, a.累計營收年增_百分比, " + \
					"b.股本_億, b.財報評分, b.年度股價_收盤, b.年度股價_平均, b.roe, b.roa, b.bps, " + \
					"c.股利所屬期間, c.股利合計, c.年均殖利率_合計, c.eps, c.盈餘分配率_合計 " + \
					"from ( select stock_no as 股票代號, mid(cast(date as char),1,4) as 年度, " + \
					"cum_revenue as 累計營收_億, ann_ins_cum_revenue_p as 累計營收年增_百分比 " + \
					"from stocks_sale_month where mid(cast(date as char),5,2) = '12' ) a " + \
					"left outer join " + \
					"( select stock_no as 股票代號, year as 年度, share_capital as 股本_億, fin_report_score as 財報評分, " + \
					"ann_stock_end_price as 年度股價_收盤, ann_stock_avg_price as 年度股價_平均, roe, roa, bps " + \
					"from STOCKS_BZ_PERFORMANCE ) b " + \
					"on a.股票代號 = b.股票代號 and a.年度 = b.年度 " + \
					"left outer join " + \
					"( select stock_no as 股票代號, period_of_dividend as 股利所屬期間, total_dividend as 股利合計, " + \
					"year_high_price as 年度股價最高價, year_low_price as 年度股價最低價, year_avg_price as 年度股價年均價, " + \
					"avg_ann_yield as 年均殖利率_合計, eps, earnings_dis_ratio as 盈餘分配率_合計 " + \
					"from STOCKS_DIVIDEND ) c " + \
					"on a.股票代號 = c.股票代號 and a.年度 = c.股利所屬期間 " + \
					"left outer join stocks_name d " + \
					"on a.股票代號 = d.stock_no " + \
					"where a.股票代號 = %s order by a.年度 desc "
	print(theSQLCmd)


	print(input_file)
	twStocksList = open(input_file, 'r')	# 預設以系統編碼開啟
	stocks = twStocksList.readlines()
	for stockNo in stocks :
		stockNo = stockNo.replace('\n','')	# 不知為何檔案會有換行符號
		print("正在處理", stockNo)
		theArgs = (stockNo,)
		print(theArgs)
#       判斷每年盈收成長率是否大於10%(連續3年)
		print(theSQLCmd)
		cursor.execute(theSQLCmd, theArgs)
		data = cursor.fetchall()
		
		if not data :
			print("No data found!!!")
		else :
			df = pd.DataFrame(data, columns=['股票代號', '股票名稱', '年度', '累計營收_億', \
				'累計營收年增_百分比', '股本_億', '財報評分', '年度股價_收盤', \
				'年度股價_平均', 'roe', 'roa', 'bps', '股利所屬期間', \
				'股利合計', '年均殖利率_合計', 'eps', '盈餘分配率_合計'])		
#			print(df[['股票代號', '年度', '累計營收年增_百分比']])

			df.fillna(value=-1, inplace = True)	# 將空值填入-1
			counts = 0		# 記錄符合條件的次數
			compTimes = DEF_COMP_TIME	# 要比對的次數

#			如果資料筆數小於預設比對次數，則不處理!!			
			if len(df.index) >= DEF_COMP_TIME and df.iloc[0,2] == '2021' :
				for num in range(0, compTimes) :

					if df.iloc[num,14] > 6.0 :
						counts += 1

					if counts == compTimes :
						output_file = stockNo + str(df.iloc[num,1]) + ".csv"
						if platform.system() != "Windows" :
							DATA_PATH = "./DATA/"
						df.to_csv(DATA_PATH + output_file, encoding="utf_8_sig")

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

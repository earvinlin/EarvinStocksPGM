"""
取得股票的盈餘成長率
syntax : GetRevenueRate.py stockNo
20240527 開發中


select 
a.stock_no, b.stock_name as '股票名稱', a.year as 年度, c.dividend_year,
a.share_capital as 股本_億, a.fin_report_score as 財報評分, c.total_dividend as '股利合計', 
a.eps_after_taxes as EPS_元_稅後EPS, (a.ann_stock_avg_price / a.eps_after_taxes) as 本益比,
a.roe, a.roa, a.bps as BPS_元_每股帳面價值, 
(1 - c.total_dividend / a.eps_after_taxes) * a.roe as 盈餘成長率,
cast(substring(c.period_of_dividend,1,2) as signed) as a1,
(cast(substring(a.year,3,2) as signed) - 1) as a2,
substring(c.period_of_dividend,3,2) as a3
from STOCKS_BZ_PERFORMANCE a
left outer join stocks_name b on a.stock_no = b.stock_no 
left outer join stocks_dividend c on a.stock_no = c.stock_no and a.year = c.dividend_year
and (substring(c.period_of_dividend,3,2) between '00' and '99' or substring(c.period_of_dividend,3,2) = 'Q4')
and c.dividend_year = a.year 
where substring(a.year,3,1) between '0' and '9' 
and a.stock_no = %s ;

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
DATA_PATH = "TEST\\"  # 20240527 程式測試中…

# 打算比對的次數
DEF_COMP_TIME = 8

input_file = "STOCKS_LIST_test.txt"
output_file = "STOCKS_REVENUE_LIST.txt"
readCnt = 0

cnx = mysql.connector.connect(user=user, password=pwd, host=host, database=db)
cursor = cnx.cursor()

try:
#    if len(sys.argv) < 2 :
#        print("You need input one parameter(fmt : theDate(yyyymmdd))")
#        print("syntax : C:\python 02_insertTaiwanDataTsecToMySQLDB.py 20170501 ")
#        sys.exit()
	theSQLCmd = "select a.stock_no, b.stock_name as '股票名稱', a.year as 年度, c.dividend_year, " + \
		"a.share_capital as 股本_億, a.fin_report_score as 財報評分, c.total_dividend as '股利合計',  " + \
		"a.eps_after_taxes as EPS_元_稅後EPS, (a.ann_stock_avg_price / a.eps_after_taxes) as 本益比, " + \
		"a.roe, a.roa, a.bps as BPS_元_每股帳面價值, " + \
		"(1 - c.total_dividend / a.eps_after_taxes) * a.roe as 盈餘成長率, " + \
		"cast(substring(c.period_of_dividend,1,2) as signed) as a1, " + \
		"(cast(substring(a.year,3,2) as signed) - 1) as a2, " + \
		"substring(c.period_of_dividend,3,2) as a3 " + \
		"from STOCKS_BZ_PERFORMANCE a " + \
		"left outer join stocks_name b on a.stock_no = b.stock_no " + \
		"left outer join stocks_dividend c on a.stock_no = c.stock_no and a.year = c.dividend_year " + \
		"and (substring(c.period_of_dividend,3,2) between '00' and '99' or substring(c.period_of_dividend,3,2) = 'Q4') " + \
		"and c.dividend_year = a.year " + \
		"left outer join taiwan_data_polaris d on a.stock_no = d.stock_no " + \
		"and d.date = (select max(date) as date from taiwan_data_polaris) " + \
		"where substring(a.year,3,1) between '0' and '9' " + \
		"and a.stock_no = %s order by a.year " 
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
			df = pd.DataFrame(data, columns=['股票代號', '股票名稱', '股利年度1', \
				 '股利年度2', '股本_億', '財報評分', '股利合計', '稅後EPS', \
				'本益比', 'roe', 'roa', '每股帳面價值', '盈餘成長率', 'a1', 'a2', ' a3'])		
#			print(df[['股票代號', '年度', '累計營收年增_百分比']])

			df.fillna(value=-999, inplace = True)	# 將空值填入-1

			output_file = stockNo + ".csv"
			print("output_file=", output_file)

			if platform.system() != "Windows" :
				DATA_PATH = "./DATA/"
			df.to_csv(DATA_PATH + output_file, encoding="utf_8_sig")
#			df.to_csv(output_file, encoding="utf_8_sig")

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

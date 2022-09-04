import mysql.connector
import datetime
import sys
import os
import csv
import numpy as np
import pandas as pd

user = 'root'
pwd  = 'lin32ledi'
host = '127.0.0.1'
db   = 'stocksdb'

"""
			// 營收成長率
			select 
			stock_no as 股票代號,
			date as 月別,
			cum_revenue as 營業收入_累計營收_億,
			ann_ins_cum_revenue_p as 營業收入_累計年增_百分比
			from stocks_sale_month
			where stock_no = '2049' and mid(cast(date as char),5,2) = '12';
			// 財報分數、每股帳面價值
			select stock_no,
			year as 年度, share_capital as 股本_億, fin_report_score as 財報評分,
			ann_stock_end_price as 年度股價_元_收盤, ann_stock_avg_price as 年度股價_元_平均,
			roe, roa, bps as BPS_元_每股帳面價值
			from STOCKS_BZ_PERFORMANCE 
			where stock_no = '2049';
			// EPS、殖利率、盈餘分配率
			select 
			stock_no as 股票代號,
			dividend_year as 股利發放年度,
			total_dividend as 股利合計,
			year_high_price as 年度股價最高價,
			year_low_price as 年度股價最低價,
			year_avg_price as 年度股價年均價,
			avg_ann_yield as 年均殖利率_合計,
			period_of_dividend as 股利所屬期間,
			eps as EPS_元,
			earnings_dis_ratio as 盈餘分配率_合計
			from STOCKS_DIVIDEND where stock_no = '2049';

"""

readCnt = 0

cnx = mysql.connector.connect(user=user, password=pwd, host=host, database=db)
cursor = cnx.cursor()

try:
#    if len(sys.argv) < 2 :
#        print("You need input one parameter(fmt : theDate(yyyymmdd))")
#        print("syntax : C:\python 02_insertTaiwanDataTsecToMySQLDB.py 20170501 ")
#        sys.exit()

	theRevenueCond = "select stock_no, date, cum_revenue, ann_ins_cum_revenue_p " + \
		"from stocks_sale_month " + \
		"where mid(cast(date as char),5,2) = %s and stock_no = %s order by date desc " 

	THE_MONTH = '12'
	input_file = "STOCKS_LIST.txt"
	print(input_file)
	twStocksList = open(input_file, 'r')	# 預設以系統編碼開啟
	stocks = twStocksList.readlines()
	for stockNo in stocks :
		stockNo = stockNo.replace('\n','')	# 不知為何檔案會有換行符號
		print("正在處理", stockNo)
		args = (THE_MONTH, (stockNo))
		print(args)
#       判斷每年盈收成長率是否大於10%(連續3年)
		print(theRevenueCond)
		cursor.execute(theRevenueCond, args)
		data = cursor.fetchall()
		
		if not data :
			print("No data found!!!")
		else :
			df = pd.DataFrame(data, columns=['股票代號', '年', '累計營收_億', '累計營收年增_百分比'])
			df2 = pd.DataFrame(df.累計營收年增_百分比 > 0)
			print("aa=" ,df2)
#		for row in cursor:
#			print(row)
		
		readCnt += 1

except mysql.connector.Error as err:
    print("insert to table 'taiwan_data_tsec' failed.")
    print("Error: {}".format(err.msg))
    sys.exit()

print("資料處理完成!! 共 " + str(readCnt) + " 筆。")
twStocksList.close()
cnx.commit()
cursor.close()
cnx.close()

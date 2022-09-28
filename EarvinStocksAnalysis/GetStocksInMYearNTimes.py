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
DATA_PATH = "DATA\\"

# 打算比對的次數
DEF_COMP_TIME = 8

input_file = "STOCKS_LIST.txt"
output_file = "M_YEAR_N_TIMES_STOCKS_LIST.txt"
readCnt = 0

cnx = mysql.connector.connect(user=user, password=pwd, host=host, database=db)
cursor = cnx.cursor()

if len(sys.argv) < 3 :
    print("You need input two parameter(fmt : M_year N_times)")
    print("syntax : C:\python 02_insertTaiwanDataTsecToMySQLDB.py 2 4 ##表示尋找2年內上漲4倍以上的股票 ")
    sys.exit()


try :
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


except mysql.connector.Error as err:
    print("Processing Error!!! ")
    print("Error: {}".format(err.msg))
    sys.exit()

print("資料處理完成!! 共 " + str(readCnt) + " 筆。")

cnx.commit()
cursor.close()
cnx.close()

import mysql.connector
import sys
import os 
import csv
import time
 
user = 'root'
pwd  = 'lin32ledi'
host = '127.0.0.1'
db   = 'stocksdb'
port = 3306

# 檔案名程格式：股票代號 + .csv
# 資料來自寶來點精靈，只處理下列欄位：日期,開盤,最高,最低,收盤,成交量,融資張數,融券張數
# 日期,開盤,最高,最低,收盤,成交量,融資張數,融券張數, 騰落指標, 外資庫存, 投信庫存, 自營商庫存, 法人庫存, 未平倉量
# 欄位：成交量/融資張數/融券張數 前面有個空白，目前要手動刪除，否則新增會失敗 
select_sql = "SELECT * FROM taiwan_data_polaris_stocks where stock_no = %s and date = %s"
delete_sql = "DELETE FROM taiwan_data_polaris_stocks where stock_no = %s and date = %s"

print("[InsertStocksFromPolarisToMySQLDB.py] 開始執行時間：" + time.strftime('%Y-%m-%d   %H:%M:%S',time.localtime()))
 
cnx = mysql.connector.connect(user=user, password=pwd, host=host, database=db)
#cnx = mysql.connector.connect(user=user, password=pwd, host=host, database=db, port=port)
cursor = cnx.cursor()
 
try:
	if len(sys.argv) < 3 :
		print("You need input two parameter(fmt : theStockNo, theFileName)")
		print("syntax : C:\python InsertStocksFromPolarisToMySQLDB.py 2002 2002.txt ")
		sys.exit()

	loadFileDir = "txt\\"
	theStockNo = sys.argv[1]
	stocks = open(loadFileDir + sys.argv[2], 'r')
	reader = csv.DictReader(stocks)
	insertCnt = 0
	deleteCnt = 0
	for row in reader :
#       print(row)
#       先查資料是否已存在，不存在要新增，存在另外處理!
#		日期要特別處理
#        theDate = int(row['日期'])
		tehDateList = row['日期'].split('/')
		theDate = int(int(tehDateList[0])-1911)*10000 + int(tehDateList[1])*100 + int(tehDateList[2])
#		print("select_sql= " + select_sql + "\n")
		cursor.execute(select_sql, (theStockNo, theDate))
		data = cursor.fetchall()
		if not data :
#           insert data to db
			theAdvanceDeclineLine = float(row['騰落指標'])
			theUpDownFirms = float(row['漲跌家數'])
			theForeignStock = float(row['外資庫存'])
			theSitAndCbStock = float(row['投信庫存'])
			theSelfEmployedStock = float(row['自營商庫存'])
			theLegalPersonStock = float(row['法人庫存'])
			theOpenInterestStock = float(row['未平倉量'])
			insertstmt=("INSERT INTO taiwan_data_polaris_stocks (stock_no, date, start_price, high_price, low_price, end_price, volume, margin_trading, short_selling, advance_decline_line, up_down_firms, foreign_stock, sit_and_cb_stock, self_employed_stock, legal_person_stock, open_interest_stock) VALUES ('%s', '%d', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f','%f','%f','%f','%f','%f')" % (theStockNo, theDate, float(row['開盤']), float(row['最高']), float(row['最低']), float(row['收盤']), float(row['成交量']), float(row['融資張數']), float(row['融券張數']), theAdvanceDeclineLine, theUpDownFirms, theForeignStock, theSitAndCbStock, theSelfEmployedStock, theLegalPersonStock, theOpenInterestStock))
			cursor.execute(insertstmt)
			insertCnt += 1
		else :
			print("Duplicate data, stock_no = " + theStockNo + ", date = " + str(theDate) + ", 融資張數= " + row['融資張數'] + ", 融券張數= " + row['融券張數'] + ", 外資庫存= " + row['外資庫存'] + ", 法人庫存= " + row['法人庫存']);
#			若資料庫已有要處理的資料，則判斷「融資張數」、「 融券張數」、「 外資庫存」及「 法人庫存」值若不為0，則刪掉資料庫該筆資料，再重新新增
#			因為抓下來的股市資料如果時間太早，當天有關融資、融券的資料會是0
			if (float(row['融資張數']) != 0 or float(row['融券張數']) != 0 or float(row['外資庫存']) != 0 or float(row['法人庫存']) != 0) :
				print("Need update")
				cursor.execute(delete_sql, (theStockNo, theDate))
				deleteCnt += 1
				
				theAdvanceDeclineLine = float(row['騰落指標'])
				theUpDownFirms = float(row['漲跌家數'])
				theForeignStock = float(row['外資庫存'])
				theSitAndCbStock = float(row['投信庫存'])
				theSelfEmployedStock = float(row['自營商庫存'])
				theLegalPersonStock = float(row['法人庫存'])
				theOpenInterestStock = float(row['未平倉量'])
				insertstmt=("INSERT INTO taiwan_data_polaris_stocks (stock_no, date, start_price, high_price, low_price, end_price, volume, margin_trading, short_selling, advance_decline_line, up_down_firms, foreign_stock, sit_and_cb_stock, self_employed_stock, legal_person_stock, open_interest_stock) VALUES ('%s', '%d', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f','%f','%f','%f','%f','%f')" % (theStockNo, theDate, float(row['開盤']), float(row['最高']), float(row['最低']), float(row['收盤']), float(row['成交量']), float(row['融資張數']), float(row['融券張數']), theAdvanceDeclineLine, theUpDownFirms, theForeignStock, theSitAndCbStock, theSelfEmployedStock, theLegalPersonStock, theOpenInterestStock))
				cursor.execute(insertstmt)
				insertCnt += 1	

except mysql.connector.Error as err:
	print("insert to table 'taiwan_data_polaris_stocks' failed.")
	print("Error: {}".format(err.msg))
	sys.exit()

print("新增資料完成!! 共 " + str(insertCnt) + " 筆。")
print("更新(刪除)資料完成!! 共 " + str(deleteCnt) + " 筆。")
stocks.close()
cnx.commit()
cursor.close()
cnx.close()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        

print("[InsertStocksFromPolarisToMySQLDB.py] 結束執行時間：" + time.strftime('%Y-%m-%d   %H:%M:%S',time.localtime()))

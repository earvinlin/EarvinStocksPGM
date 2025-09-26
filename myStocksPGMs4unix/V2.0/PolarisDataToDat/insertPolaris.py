import mysql.connector
import sys
import os 
import csv
 
user = 'root'
pwd  = 'lin32ledi'
host = '127.0.0.1'
db   = 'stocksdb'
 
select_sql = "SELECT * FROM taiwan_data_polaris_old_to1060818 where date = %s"
 
cnx4select = mysql.connector.connect(user=user, password=pwd, host=host, database=db)
selectCursor = cnx4select.cursor()
cnx4insert = mysql.connector.connect(user=user, password=pwd, host=host, database=db)
insertCursor = cnx4insert.cursor()
 
try:
	if len(sys.argv) < 2 :
		print("You need input two parameter(fmt : theDate)")
		print("syntax : C:\python InsertPolaris.py stocks.csv ")
		sys.exit()

	stocks = open(sys.argv[1], 'r')
	reader = csv.DictReader(stocks)
	totalInsertCount = 0

	for row in reader :
		theDate = row['date']
		print("Processing date is " + theDate)
		insertCount = 0
		
		selectCursor.execute(select_sql, (theDate,))	
		for (theDATE, theSTOCK_NO, theSTOCK_NAME, theSTART_PRICE, theHIGH_PRICE, theLOW_PRICE, theEND_PRICE, theUP_DOWN, theVOLUME, theHIGHEST_PRICE, theLOWEST_PRICE) in selectCursor :
			print("DATE=" + theDATE + ", STOCK_NO= " + theSTOCK_NO + ",START_PRICE= " + str(theSTART_PRICE) + ", HIGH_PRICE= " + str(theHIGH_PRICE))

			insertStmt=("INSERT INTO TAIWAN_DATA_POLARIS (DATE, STOCK_NO, STOCK_NAME, START_PRICE, HIGH_PRICE, LOW_PRICE, END_PRICE, UP_DOWN, VOLUME, HIGHEST_PRICE, LOWEST_PRICE) VALUES ('%i', '%s', '%s', '%f', '%f', '%f', '%f', '%s', '%f', '%f', '%f')" % (int(theDATE), theSTOCK_NO, theSTOCK_NAME, float(theSTART_PRICE), float(theHIGH_PRICE), float(theLOW_PRICE), float(theEND_PRICE), theUP_DOWN, float(theVOLUME), float(theHIGHEST_PRICE), float(theLOWEST_PRICE)))
			insertCursor.execute(insertStmt)
			insertCount += 1
			totalInsertCount += 1
		cnx4insert.commit()

except mysql.connector.Error as err:
	print("insert to table 'taiwan_data_polaris_stocks' failed.")
	print("Error: {}".format(err.msg))
	sys.exit()

print("新增資料完成!! 共 " + str(totalInsertCount) + " 筆。")
stocks.close()
cnx4select.commit()
# cnx4insert.commit()
selectCursor.close()
insertCursor.close()
cnx4select.close()
cnx4insert.close()


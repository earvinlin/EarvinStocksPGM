import mysql.connector
import datetime
import sys
import os
import csv

user = 'root'
pwd  = 'lin32ledi'
host = '127.0.0.1'
db   = 'stocksdb'

# 郎祘Α絃计_yymm.txt
# 戈ㄓ靡ユ┮呼逆ら戳, 秨絃计, 程蔼计, 程计, Μ絃计
select_sql = "SELECT * FROM taiwan_data_tsec where date = %s"

cnx = mysql.connector.connect(user=user, password=pwd, host=host, database=db)
cursor = cnx.cursor()

try:
    if len(sys.argv) < 2 :
        print("You need input one parameter(fmt : theDate(yyyymmdd))")
        print("syntax : C:\python 02_insertTaiwanDataTsecToMySQLDB.py 20170501 ")
        sys.exit()

    saveFileDir = "絃计\\"
    input_file = "絃计_" + sys.argv[1] + ".txt"
    print(input_file)
    tsec = open(saveFileDir + input_file, 'r')	# 箇砞╰参絪絏秨币
    reader = csv.DictReader(tsec, delimiter=',')
	
    THE_STOCK_NO = 'taiex'
    THE_STOCK_NAME ='絃计'

    insertCnt = 0
    for row in reader :
#       琩戈琌璶ノ穝ぃノ穝糤!!
#		NOTE : parse ら戳 yy/mm/dd
        tehDateList = row['ら戳'].split('/')
        theDate = str(int(tehDateList[0])+1911) + "/" + str(tehDateList[1]) + "/" + str(tehDateList[2])
        print("ユら戳= " + theDate)
        theTradeDate = datetime.date((int(tehDateList[0])+1911), int(tehDateList[1]), int(tehDateList[2]))
        cursor.execute(select_sql, (theTradeDate,))
        data = cursor.fetchall()

        if not data :
#           insert data to db
            theStartPrice = float(row['秨絃计'].replace(',', ''))
            theHighPrice = float(row['程蔼计'].replace(',', ''))
            theLowPrice = float(row['程计'].replace(',', ''))
            theEndPrice = float(row['Μ絃计'].replace(',', ''))
            insertstmt=("INSERT INTO taiwan_data_tsec (stock_no, date, stock_name, start_price, high_price, low_price, end_price) VALUES ('%s', '%s', '%s', '%f', '%f', '%f', '%f')" % (THE_STOCK_NO, theTradeDate, THE_STOCK_NAME, theStartPrice, theHighPrice, theLowPrice, theEndPrice))
            cursor.execute(insertstmt)
            insertCnt += 1
        else :
            print("Duplicate data, stock_no = " + THE_STOCK_NO + ", date = " + str(theTradeDate));

except mysql.connector.Error as err:
    print("insert to table 'taiwan_data_tsec' failed.")
    print("Error: {}".format(err.msg))
    sys.exit()

print("穝糤戈ЧΘ!!  " + str(insertCnt) + " 掸")
tsec.close()
cnx.commit()
cursor.close()
cnx.close()

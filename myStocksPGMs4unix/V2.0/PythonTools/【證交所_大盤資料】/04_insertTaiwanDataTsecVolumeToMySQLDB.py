import mysql.connector
import datetime
import sys
import os
import csv

user = 'root'
pwd  = 'lin32ledi'
host = '127.0.0.1'
db   = 'stocksdb'

# 檔案名程格式：大盤成交量_yyyymmdd.txt
# 資料來自證交所網站，包含下列欄位：日期, 成交股數, 成交金額, 成交筆數, 發行量加權股價指數, 漲跌點數
select_sql = "SELECT * FROM taiwan_data_tsec_volume where date = %s"

cnx = mysql.connector.connect(user=user, password=pwd, host=host, database=db)
cursor = cnx.cursor()

try:
    if len(sys.argv) < 2 :
#        print("You need input two parameter(fmt : theSelectYear(民國年，長度為2或3) theSelectMonth(月份，不足2位前面補0)) ")
#        print("syntax : C:\python 04_insertTaiwanDataTsecVolumeToMySQLDB.py 106 04 ")
        print("You need input one parameter(fmt : yyyymmdd ")
        print("syntax : C:\python 04_insertTaiwanDataTsecVolumeToMySQLDB.py 20170501 ")
        sys.exit()

    saveFileDir = "大盤成交量\\"
    input_file = "大盤成交量_" + sys.argv[1] + ".txt"
    print(input_file)
    tsec = open(saveFileDir + input_file, 'r')	# 預設以系統編碼開啟
    reader = csv.DictReader(tsec, delimiter=',')

    insertCnt = 0
    for row in reader :
#       先查資料是否已存在，存在要用更新；不存在用新增!!
#		NOTE : parse 日期 yy/mm/dd
        tehDateList = row['日期'].split('/')
        theDate = str(int(tehDateList[0])+1911) + "/" + str(tehDateList[1]) + "/" + str(tehDateList[2])
        print("交易日期= " + theDate)
        theTradeDate = datetime.date((int(tehDateList[0])+1911), int(tehDateList[1]), int(tehDateList[2]))
        cursor.execute(select_sql, (theTradeDate,))
        data = cursor.fetchall()

        if not data :
#           insert data to db
#           日期;成交股數;成交金額;成交筆數;發行量加權股價指數;漲跌點數;
            theVolume = float(row['成交股數'].replace(',', '')) / 1000
            theAmount = float(row['成交金額'].replace(',', '')) / 1000
            theRecords = float(row['成交筆數'].replace(',', ''))
            theIndex = float(row['發行量加權股價指數'].replace(',', ''))
            theUpDown = float(row['漲跌點數'].replace(',', ''))
            print("theVolume=" + str(theVolume) + ", theAmount= " + str(theAmount) + ", theRecords= " + str(theRecords) + ", theIndex= " + str(theIndex));
            insertstmt=("INSERT INTO taiwan_data_tsec_volume (`date`, `volume`, `amount`, `records`, `index`, `updown`) VALUES ('%s', '%f', '%f', '%f', '%f', '%f')" % (theTradeDate, theVolume, theAmount, theRecords, theIndex, theUpDown))
            cursor.execute(insertstmt)
            insertCnt += 1
        else :
            print("Duplicate data, the trade_date = " + str(theTradeDate));

except mysql.connector.Error as err:
    print("insert to table 'taiwan_data_tsec_volume' failed.")
    print("Error: {}".format(err.msg))
    sys.exit()

print("新增資料完成!! 共 " + str(insertCnt) + " 筆。")
tsec.close()
cnx.commit()
cursor.close()
cnx.close()

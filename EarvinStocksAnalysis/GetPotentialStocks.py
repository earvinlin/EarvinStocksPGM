import mysql.connector
import datetime
import sys
import os
import csv

user = 'root'
pwd  = 'lin32ledi'
host = '127.0.0.1'
db   = 'stocksdb'

# �ɮצW�{�榡�G�j�L����_yymm.txt
# ��ƨӦ��ҥ�Һ����A�]�t�U�C���G���, �}�L����, �̰�����, �̧C����, ���L����
select_sql = "SELECT * FROM taiwan_data_tsec where date = %s"

cnx = mysql.connector.connect(user=user, password=pwd, host=host, database=db)
cursor = cnx.cursor()

try:
    if len(sys.argv) < 2 :
        print("You need input one parameter(fmt : theDate(yyyymmdd))")
        print("syntax : C:\python 02_insertTaiwanDataTsecToMySQLDB.py 20170501 ")
        sys.exit()

    saveFileDir = "�j�L����\\"
    input_file = "�j�L����_" + sys.argv[1] + ".txt"
    print(input_file)
    tsec = open(saveFileDir + input_file, 'r')	# �w�]�H�t�νs�X�}��
    reader = csv.DictReader(tsec, delimiter=',')
	
    THE_STOCK_NO = 'taiex'
    THE_STOCK_NAME ='�j�L����'

    insertCnt = 0
    for row in reader :
#       ���d��ƬO�_�w�s�b�A�s�b�n�Χ�s�F���s�b�ηs�W!!
#		NOTE : parse ��� yy/mm/dd
        tehDateList = row['���'].split('/')
        theDate = str(int(tehDateList[0])+1911) + "/" + str(tehDateList[1]) + "/" + str(tehDateList[2])
        print("������= " + theDate)
        theTradeDate = datetime.date((int(tehDateList[0])+1911), int(tehDateList[1]), int(tehDateList[2]))
        cursor.execute(select_sql, (theTradeDate,))
        data = cursor.fetchall()

        if not data :
#           insert data to db
            theStartPrice = float(row['�}�L����'].replace(',', ''))
            theHighPrice = float(row['�̰�����'].replace(',', ''))
            theLowPrice = float(row['�̧C����'].replace(',', ''))
            theEndPrice = float(row['���L����'].replace(',', ''))
            insertstmt=("INSERT INTO taiwan_data_tsec (stock_no, date, stock_name, start_price, high_price, low_price, end_price) VALUES ('%s', '%s', '%s', '%f', '%f', '%f', '%f')" % (THE_STOCK_NO, theTradeDate, THE_STOCK_NAME, theStartPrice, theHighPrice, theLowPrice, theEndPrice))
            cursor.execute(insertstmt)
            insertCnt += 1
        else :
            print("Duplicate data, stock_no = " + THE_STOCK_NO + ", date = " + str(theTradeDate));

except mysql.connector.Error as err:
    print("insert to table 'taiwan_data_tsec' failed.")
    print("Error: {}".format(err.msg))
    sys.exit()

print("�s�W��Ƨ���!! �@ " + str(insertCnt) + " ���C")
tsec.close()
cnx.commit()
cursor.close()
cnx.close()

import mysql.connector
import sys
import os
import csv

user = 'root'
pwd  = 'lin32ledi'
host = '127.0.0.1'
db   = 'stocksdb'

input_file = 'stocks.txt'

#select_sql = "SELECT id, name, age FROM mytable"

cnx = mysql.connector.connect(user=user, password=pwd, host=host, database=db)
cursor = cnx.cursor()

try:
#    cursor.execute(create_table_sql)
    theDate = int(sys.argv[1])
    thePERatio = 0.0
    theYields = 0.0
    thePBratio = 0.0
# 沒有輸入檔名的話，預設是處理stocks.txt
    if len(sys.argv) > 2 :
    	input_file = sys.argv[2]

    stocks = open(input_file, 'r')
    reader = csv.DictReader(stocks, delimiter=';')
    for row in reader :
        print(row)
        if row['本益比'] == '-' :
        	thePERatio = 0
        else :
        	thePERatio = float(row['本益比'])
        if row['殖利率(%)'] == '-' :
        	theYields = 0
        else :
        	theYields = float(row['殖利率(%)'])
        if row['股價淨值比'] == '-' :
        	thePBratio = 0
        else :
        	thePBratio = float(row['股價淨值比'])
#       insert data to db
        insertstmt=("INSERT INTO taiwan_data_stocks_daily_ratios (date, stock_no, stock_name, pe_ratio, yields, pb_ratio) VALUES ('%d', '%s', '%s', '%f', '%f', '%f')" % (theDate, row['證券代號'], row['證券名稱'], thePERatio, theYields, thePBratio))
        cursor.execute(insertstmt)

except mysql.connector.Error as err:
    print("insert record 'taiwan_data_stocks_daily_ratios' failed.")
    print("Error: {}".format(err.msg))
    sys.exit()





'''
try:
    cursor.execute(insert_sql)
except mysql.connector.Error as err:
    print("insert table 'mytable' failed.")
    print("Error: {}".format(err.msg))
    sys.exit()

if os.path.exists(data_file):
    myfile = open(data_file)
    lines = myfile.readlines()
    myfile.close()

    for line in lines:
        myset = line.split()
        sql = "INSERT INTO mytable (name, age) VALUES ('{}', {})".format(myset[0], myset[1])
        try:
            cursor.execute(sql)
        except mysql.connector.Error as err:
            print("insert table 'mytable' from file 'mysql-test.dat' -- failed.")
            print("Error: {}".format(err.msg))
            sys.exit()

try:
    cursor.execute(select_sql)
    for (id, name, age) in cursor:
        print("ID:{}  Name:{}  Age:{}".format(id, name, age))
except mysql.connector.Error as err:
    print("query table 'mytable' failed.")
    print("Error: {}".format(err.msg))
    sys.exit()
'''

stocks.close()
cnx.commit()
cursor.close()
cnx.close()

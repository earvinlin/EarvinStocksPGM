"""
傳入的參數為要處理的股票代號
產出的檔案名稱為股票代號(沒有副檔案)
"""
import mysql.connector
import sys
import os 
 
user = 'root'
pwd  = 'lin32ledi'
host = '127.0.0.1'
db   = 'stocksdb'

def GetStocksData(stockNo) :
    # 欄位順序：日期,開盤,最高,最低,收盤, 成交量
    select_sql = "SELECT DATE, START_PRICE, HIGH_PRICE, LOW_PRICE, END_PRICE, VOLUME FROM TAIWAN_DATA_POLARIS_STOCKS WHERE STOCK_NO = %s ORDER BY DATE "
    cnx = mysql.connector.connect(user=user, password=pwd, host=host, database=db)
    cursor = cnx.cursor()
    values = []
    try:
        insertCnt = 0
        cursor.execute(select_sql, (stockNo, ))
        for row in cursor:
            outStr = ""
            for i in range(len(row)) :
                outStr += str(row[i]) + ","
            values.append(outStr)
#            print(outStr[0:len(outStr)-1])
    except mysql.connector.Error as err:
        sys.exit()

#    stocks.close()
    cursor.close()
    cnx.close()
    return values




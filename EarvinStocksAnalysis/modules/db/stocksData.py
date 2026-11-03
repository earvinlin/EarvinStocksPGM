"""
傳入的參數為要處理的股票代號
產出的檔案名稱為股票代號(沒有副檔案)
"""
import mysql.connector
import pandas as pd
import numpy as np

# 不好的做法，應該要搬走
user = 'root'
pwd  = 'lin32ledi'
host = '127.0.0.1'
db   = 'stocksdb'

def getStocksData(stockNo) :
    # 欄位順序：日期,開盤,最高,最低,收盤, 成交量
    select_sql = "SELECT DATE, START_PRICE, HIGH_PRICE, LOW_PRICE, END_PRICE, VOLUME FROM TAIWAN_DATA_POLARIS WHERE STOCK_NO = %s ORDER BY DATE "
    cnx = mysql.connector.connect(user=user, password=pwd, host=host, database=db)
    cursor = cnx.cursor()
    stocksData = []
    try:
        insertCnt = 0
        cursor.execute(select_sql, (stockNo, ))
        for row in cursor:
            rsData = []
            for i in range(len(row)) :
                rsData.append(row[i])
            stocksData.append(rsData)
    except mysql.connector.Error as err:
        sys.exit()

    cursor.close()
    cnx.close()
    rtnData = pd.DataFrame(stocksData, columns=['trade_date', 'start_price', 'high_price', 'low_price', 'end_price', 'volume'])
    rtnData.index = list(rtnData['trade_date'])
    return rtnData

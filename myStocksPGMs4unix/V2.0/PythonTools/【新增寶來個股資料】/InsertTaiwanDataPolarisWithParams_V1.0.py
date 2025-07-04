import mysql.connector
import sys
import os 

user = 'root'
pwd  = 'lin32ledi'
host = '127.0.0.1'
db   = 'stocksdb'

# 代號, 名稱, 開盤, 最高, 最低, 收盤, 漲跌, 成交量, 漲停價, 跌停價

select_sql = "SELECT * FROM taiwan_data_polaris where date = %s and stock_no = %s "
cnx = mysql.connector.connect(user=user, password=pwd, host=host, database=db)
cursor = cnx.cursor()

try :
    if len(sys.argv) < 2 :
        print("You need input one parameter(fmt : theFileName)")
        print("syntax : C:\python 01_taiwanDataPolarisWithParams.py Close20170330 ")
        sys.exit()

    insertCnt = 0
    theFileName = sys.argv[1]
    input_file = theFileName + ".TXT"

    theTradeDate = str(int(int(theFileName[5:9])-1911)*10000 + int(theFileName[9:11])*100 + int(theFileName[11:]))
    print("The trade date is " + theTradeDate)
    
#   Windows預設為CP950編碼 (在Windows會跳行<應該是windows 與 unix的換行符號不同所致!!>)  
    with open(input_file, 'r', encoding = 'CP950') as infile :
        for each_line in infile :   
            theStockNo = each_line[0:10]
            theInData = each_line[10:].split(" ")
            theStockData = []
            for s in theInData :
                if len(s) > 0 : 
                    theStockData.append(s)
            theStockName = str(theStockData[0]).strip() 
            theStartPrice = float(theStockData[1]) 
            theHighPrice = float(theStockData[2]) 
            theLowPrice = float(theStockData[3]) 
            theEndPrice = float(theStockData[4]) 
            theUpDown = str(theStockData[5]) 
            theVolume = float(theStockData[6]) 
            theHighestPrice = float(theStockData[7]) 
            theLowestPrice = float(theStockData[8])                    

#---------- process about db section STR ---------------------------------------
            cursor.execute(select_sql, (theTradeDate, theStockNo))
            data = cursor.fetchall()
            if not data :
#               insert data to db
                print("Prepare to insret, Date = " + theTradeDate + " ,StockName = " + theStockName)
                insertstmt = ("INSERT INTO taiwan_data_polaris (date, stock_no, stock_name, start_price, high_price, low_price, end_price, up_down, volume, highest_price, lowest_price) VALUES ('%s', '%s', '%s', '%f', '%f', '%f', '%f', '%s', '%f', '%f', '%f')" % (theTradeDate, theStockNo, theStockName, theStartPrice, theHighPrice, theLowPrice, theEndPrice, theUpDown, theVolume, theHighestPrice, theLowestPrice))
                cursor.execute(insertstmt)
                insertCnt += 1
            else :
                print("Duplicate data, Date = " + theTradeDate + ", StockNo = " + theStockNo);
#   不加此行新增會失敗~~
    cnx.commit()
#---------- process about db section END ---------------------------------------
    print('資料處理完成!!共' + str(insertCnt) + '筆。') 

except mysql.connector.Error as err:
    print("Insert table [taiwan_data_polaris] failed.")
    print("Error: {}".format(err.msg))
    sys.exit()
except IOError as err :
    print('File error : ' + str(err))
finally:
    cursor.close()
    cnx.close()
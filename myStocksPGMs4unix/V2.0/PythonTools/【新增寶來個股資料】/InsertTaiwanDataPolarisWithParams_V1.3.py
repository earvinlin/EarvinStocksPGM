import mysql.connector
import sys
import os 
import unicodedata
import datetime

user = 'root'
pwd  = 'lin32ledi'
host = '127.0.0.1'
db   = 'stocksdb'

def slice_display_width(s, start, end):
    result = []
    width = 0
    for ch in s:
        w = 2 if unicodedata.east_asian_width(ch) in ('F','W') else 1
        if start <= width < end:
            result.append(ch)
        width += w
    return ''.join(result)

select_sql = "SELECT * FROM taiwan_data_polaris where date = %s and stock_no = %s "
cnx = mysql.connector.connect(user=user, password=pwd, host=host, database=db)
cursor = cnx.cursor()

try:
    if len(sys.argv) < 2:
        print("You need input one parameter(fmt : theFileName)")
        print("syntax : C:\\python InsertTaiwanDataPolarisWithParams_V1.3.py Close20260211 ")
        sys.exit()

    saveFileDir = "Files\\"
    totalCnt = 0
    insertCnt = 0
    errorCnt = 0
    theFileName = sys.argv[1]
    input_file = theFileName + ".TXT"
    theTradeDate = int(int(theFileName[5:9])-1911)*10000 + int(theFileName[9:11])*100 + int(theFileName[11:])
    print("The trade date is " + str(theTradeDate))

    # 開啟錯誤紀錄檔案
    error_log_path = "error_log.txt"
    error_file = open(error_log_path, "a", encoding="utf-8")

    with open(saveFileDir + input_file, 'r', encoding='CP950') as infile:
        for each_line in infile:
            try:
                theStockNo = slice_display_width(each_line, 0, 10).strip()
                theStockName = slice_display_width(each_line, 10, 30).strip()
                theStartPrice = float(slice_display_width(each_line, 30, 40).strip())
                theHighPrice = float(slice_display_width(each_line, 40, 50).strip())
                theLowPrice = float(slice_display_width(each_line, 50, 60).strip())
                theEndPrice = float(slice_display_width(each_line, 60, 70).strip())
                theUpDown = slice_display_width(each_line, 70, 80).strip()
                theVolume = float(slice_display_width(each_line, 80, 90).strip())
                theHighestPrice = float(slice_display_width(each_line, 90, 100).strip())
                theLowestPrice = float(slice_display_width(each_line, 100, 110).strip())

                print(theStockNo,", ", theStockName, ", ",theStartPrice, ", ",
                      theHighPrice, ", ",theLowPrice, ", ",theEndPrice, ", ",
                      theUpDown, ", ",theVolume, ", ", theHighestPrice, ", ",theLowestPrice)

                cursor.execute(select_sql, (theTradeDate, theStockNo))
                data = cursor.fetchall()
                if not data:
                    print("Prepare to insert, Date = " + str(theTradeDate) + " ,StockName = " + theStockName)
                    insertstmt = ("INSERT INTO taiwan_data_polaris "
                                  "(date, stock_no, stock_name, start_price, high_price, low_price, end_price, up_down, volume, highest_price, lowest_price) "
                                  "VALUES ('%i', '%s', '%s', '%f', '%f', '%f', '%f', '%s', '%f', '%f', '%f')" %
                                  (theTradeDate, theStockNo, theStockName, theStartPrice, theHighPrice, theLowPrice, theEndPrice, theUpDown, theVolume, theHighestPrice, theLowestPrice))
                    cursor.execute(insertstmt)
                    insertCnt += 1
                else:
                    print("Duplicate data, Date = " + str(theTradeDate) + ", each_line= " + each_line)
                    error_file.write(f"{datetime.datetime.now()} | Duplicate data | Date={theTradeDate} | Line={each_line}\n")
                    errorCnt += 1
            except ValueError as err:
                print('File error2 : ' + str(err) + ", each_line= " + each_line)
                error_file.write(f"{datetime.datetime.now()} | ValueError: {err} | Line={each_line}\n")
                errorCnt += 1

            totalCnt += 1

    cnx.commit()
    error_file.close()

    print('資料處理完成!! 處理 ' + str(totalCnt) + '筆，新增成功 ' + str(insertCnt) + ' 筆， 錯誤 ' + str(errorCnt) + '筆')

except mysql.connector.Error as err:
    print("Insert table [taiwan_data_polaris] failed.")
    print("Error: {}".format(err.msg))
    sys.exit()
except IOError as err:
    print('File error1 : ' + str(err))
except ValueError as err:
    print('File error2 : ' + str(err) + ", each_line= " + each_line)
finally:
    cursor.close()
    cnx.close()
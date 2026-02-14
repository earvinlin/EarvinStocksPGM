import mysql.connector
import datetime
import sys
import os
import csv
from datetime import datetime as dt, timedelta

user = 'root'
pwd  = 'lin32ledi'
host = '127.0.0.1'
db   = 'stocksdb'

select_sql = "SELECT * FROM taiwan_data_tsec_margin WHERE date = %s AND type = %s"

cnx = mysql.connector.connect(user=user, password=pwd, host=host, database=db)
cursor = cnx.cursor()

try:
    if len(sys.argv) < 3:
        print("You need input two parameters (fmt : yyyymmdd yyyymmdd)")
        print("syntax : python MS_insertTaiwanDataTsecMarginToMySQLDB_v2.py 20260201 20260211")
        sys.exit()

    start_date_str = sys.argv[1]
    end_date_str = sys.argv[2]

    try:
        start_date = dt.strptime(start_date_str, "%Y%m%d")
        end_date = dt.strptime(end_date_str, "%Y%m%d")
    except ValueError:
        print("日期格式錯誤，請使用 yyyymmdd")
        sys.exit()

    if start_date > end_date:
        print("開始日期不可大於結束日期")
        sys.exit()

    saveFileDir = "大盤融資融券\\"
    total_insert = 0

    current = start_date
    while current <= end_date:
        date_str = current.strftime("%Y%m%d")
        input_file = f"大盤融資融券_{date_str}.txt"
        full_path = os.path.join(saveFileDir, input_file)

        print(f"\n處理檔案：{input_file}")

        if not os.path.exists(full_path):
            print("  !!! 檔案不存在，跳過")
            current += timedelta(days=1)
            continue

        try:
            with open(full_path, 'r', encoding="utf-8", errors="ignore") as tsec:
                reader = csv.DictReader(tsec, delimiter=',')

                # 日期轉換
                theTradeDate = dt.strptime(date_str, "%Y%m%d").date()

                insertCnt = 0
                for row in reader:
                    theType = "3"
                    if row['項目'] == "融資(交易單位)":
                        theType = "1"
                    elif row['項目'] == "融券(交易單位)":
                        theType = "2"

                    cursor.execute(select_sql, (theTradeDate, theType))
                    data = cursor.fetchall()

                    if not data:
                        theBuy = float(row['買進'].replace(',', ''))
                        theSell = float(row['賣出'].replace(',', ''))
                        theReturn = float(row['現金(券)償還'].replace(',', ''))
                        theYes_balance = float(row['前日餘額'].replace(',', ''))
                        theBalance = float(row['今日餘額'].replace(',', ''))

                        insert_sql = (
                            "INSERT INTO taiwan_data_tsec_margin "
                            "(`date`, `type`, `buy`, `sell`, `return`, `yes_balance`, `balance`) "
                            "VALUES (%s, %s, %s, %s, %s, %s, %s)"
                        )
                        cursor.execute(insert_sql, (
                            theTradeDate, theType, theBuy, theSell, theReturn, theYes_balance, theBalance
                        ))
                        insertCnt += 1
                    else:
                        print(f"  Duplicate: date={theTradeDate}, type={theType}")

                cnx.commit()
                print(f"  → 新增 {insertCnt} 筆")
                total_insert += insertCnt

        except Exception as e:
            print("  !!! File Error:", e)

        current += timedelta(days=1)

except mysql.connector.Error as err:
    print("insert to table 'taiwan_data_tsec_margin' failed.")
    print("Error: {}".format(err.msg))
    sys.exit()

print(f"\n全部日期處理完畢，共新增 {total_insert} 筆資料")
cursor.close()
cnx.close()
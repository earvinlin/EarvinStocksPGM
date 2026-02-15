import mysql.connector
import sys
import os
import csv
from datetime import datetime, timedelta

# -----------------------------
# DB 設定
# -----------------------------
user = 'root'
pwd  = 'lin32ledi'
host = '127.0.0.1'
db   = 'stocksdb'

select_sql = "SELECT * FROM taiwan_data_stocks_daily_ratios WHERE stock_no = %s AND date = %s"

def open_text_file_safely(path):
    # 先試 CP950：如果 open + read 都成功，就用 CP950
    try:
        with open(path, 'r', encoding='cp950') as f:
            f.read()
        print("  使用 CP950 解碼")
        return open(path, 'r', encoding='cp950')
    except UnicodeDecodeError:
        # CP950 失敗，改用 UTF-8 再試一次
        with open(path, 'r', encoding='utf8') as f:
            f.read()
        print("  使用 UTF-8 解碼")
        return open(path, 'r', encoding='utf8')

# -----------------------------
# 參數檢查
# -----------------------------
if len(sys.argv) < 3:
    print("You need input two parameters (fmt: yyyymmdd yyyymmdd)")
    print("syntax : python3 03_insertDailyRatiosToMySQLDB_v2.py 20050902 20050930")
    sys.exit()

start_date_str = sys.argv[1]
end_date_str = sys.argv[2]

try:
    start_date = datetime.strptime(start_date_str, "%Y%m%d")
    end_date = datetime.strptime(end_date_str, "%Y%m%d")
except ValueError:
    print("日期格式錯誤，請使用 yyyymmdd")
    sys.exit()

if start_date > end_date:
    print("開始日期不可大於結束日期")
    sys.exit()

# -----------------------------
# DB 連線
# -----------------------------
cnx = mysql.connector.connect(user=user, password=pwd, host=host, database=db)
cursor = cnx.cursor()

# 判斷程式是在何種作業系統執行以確認路徑撰寫方式
save_dir = ""
if sys.platform == "darwin" or sys.platform == "linux" :
    save_dir = "Files/"
else :
    save_dir = "Files\\"

# -----------------------------
# 主迴圈：逐日處理
# -----------------------------
current = start_date
total_insert = 0

while current <= end_date:

    date_str = current.strftime("%Y%m%d")
    input_file = f"stocks_個股日本益比殖利率及股價淨值比-{date_str}.txt"
    full_path = save_dir + input_file

    print(f"\n處理日期：{date_str}")
    print(f"讀取檔案：{input_file}")

    if not os.path.exists(full_path):
        print("  !!! 檔案不存在，跳過")
        current += timedelta(days=1)
        continue

    try:
        stocks = open_text_file_safely(full_path)

        reader = csv.DictReader(stocks, delimiter=',')

        insertCnt = 0

        for row in reader:
            # 數值欄位處理
            pe = 0.0 if row['本益比'] == '-' else float(row['本益比'].replace(",", ""))
            yields = 0.0 if row['殖利率(%)'] == '-' else float(row['殖利率(%)'].replace(",", ""))
            pb = 0.0 if row['股價淨值比'] == '-' else float(row['股價淨值比'].replace(",", ""))

            # 查重 ; 日期轉換為民國年 [ (int(date_str) - 19110000) ]
            cursor.execute(select_sql, (row['證券代號'], (int(date_str) - 19110000)))
            data = cursor.fetchall()

            if not data:
                insert_sql = (
                    "INSERT INTO taiwan_data_stocks_daily_ratios "
                    "(date, stock_no, stock_name, pe_ratio, yields, pb_ratio) "
                    "VALUES (%s, %s, %s, %s, %s, %s)"
                )
                cursor.execute(insert_sql, (
                    (int(date_str) - 19110000),
                    row['證券代號'],
                    row['證券名稱'],
                    pe,
                    yields,
                    pb
                ))
                insertCnt += 1
            else:
                print(f"  Duplicate: date={date_str}, stock_no={row['證券代號']}")

        stocks.close()
        cnx.commit()

        print(f"  → 新增 {insertCnt} 筆")
        total_insert += insertCnt

    except mysql.connector.Error as err:
        print("  !!! DB Error:", err.msg)

    except Exception as e:
        print("  !!! File Error:", e)

    current += timedelta(days=1)

# -----------------------------
# 結束
# -----------------------------
cursor.close()
cnx.close()

print("\n全部日期處理完畢")
print(f"總共新增 {total_insert} 筆資料")
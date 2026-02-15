import re
import sys
import urllib.request
import urllib.parse
import ssl
from datetime import datetime, timedelta

# -----------------------------
# 參數檢查
# -----------------------------
if len(sys.argv) < 3:
    print("You need input two parameters (fmt: yyyymmdd yyyymmdd)")
    print("syntax : python 01_getStocksDailyRatiosData_v2.py 20220101 20220131")
    sys.exit()

start_date_str = sys.argv[1]
end_date_str = sys.argv[2]

print(f"input start = {start_date_str}")
print(f"input end   = {end_date_str}\n")

# -----------------------------
# 日期轉換
# -----------------------------
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
# SSL 設定
# -----------------------------
ssl._create_default_https_context = ssl._create_unverified_context

# -----------------------------
# 逐日抓取資料
# -----------------------------
save_dir = ""
if sys.platform == "darwin" or sys.platform == "linux" :
    save_dir = "Files/"
else :
    save_dir = "Files\\"

current = start_date
while current <= end_date:

    date_str = current.strftime("%Y%m%d")
    print(f"處理日期：{date_str}")

    url = f"https://www.twse.com.tw/exchangeReport/BWIBBU_d?response=csv&date={date_str}&selectType=ALL"

    try:
        f = urllib.request.urlopen(url)
        content = f.read().decode('CP950')

        file_name = f"stocks_個股日本益比殖利率及股價淨值比-{date_str}.txt"
        print(f"  儲存檔案：{file_name}")

        with open(save_dir + file_name, "w", encoding="utf-8") as out:
            out.write(content)

        print("  → 資料儲存完成\n")

    except Exception as err:
        print(f"  !!! 抓取失敗：{err}\n")

    current += timedelta(days=1)

print("全部日期處理完畢！")
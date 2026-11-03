import re
import sys
import shutil
from datetime import datetime, timedelta

# -----------------------------
# 參數檢查
# -----------------------------
if len(sys.argv) < 3:
    print("You need input two parameters (fmt: yyyymmdd yyyymmdd)")
    print("syntax : python 02_formatStocksDailyRatiosData_v2.py 20050902 20260211")
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
# 主程式：逐日處理
# -----------------------------
save_dir = ""
if sys.platform == "darwin" or sys.platform == "linux" :
    save_dir = "Files/"
else :
    save_dir = "Files\\"

current = start_date
while current <= end_date:

    date_str = current.strftime("%Y%m%d")
    file_name = f"stocks_個股日本益比殖利率及股價淨值比-{date_str}.txt"
    bk_file_name = f"BK_{file_name}"

    print(f"處理檔案：{file_name}")

    try:
        # 備份原始檔案
        shutil.copy(save_dir + file_name, save_dir + bk_file_name)

        # 讀取備份檔
        with open(save_dir + bk_file_name, 'r', encoding="utf-8") as infile:
            data = infile.readlines()

        # 過濾資料
        filtered = []
        for line in data:
            if re.findall(r'^"\d{4}', line) or re.findall(r'^"證券代號', line):
                filtered.append(line)

        # 寫回原檔
        with open(save_dir + file_name, 'w', encoding="utf-8") as outfile:
            outfile.writelines(filtered)

        print(f"  → {date_str} 格式化完成\n")

    except IOError as err:
        print(f"  !!! 檔案處理失敗：{err}\n")

    current += timedelta(days=1)

print("全部日期格式化處理完畢！")
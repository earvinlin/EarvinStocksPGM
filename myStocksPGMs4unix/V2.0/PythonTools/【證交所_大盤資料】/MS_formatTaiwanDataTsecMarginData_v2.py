import re
import sys
import shutil
from datetime import datetime, timedelta
import os

# -----------------------------
# 參數檢查
# -----------------------------
if len(sys.argv) < 4:
    print("You need input three parameters (fmt: yyyymmdd yyyymmdd type)")
    print("syntax : python MS_formatTaiwanDataTsecMarginData_v2.py 20260201 20260211 MS")
    sys.exit()

start_date_str = sys.argv[1]
end_date_str = sys.argv[2]
trade_type = sys.argv[3]

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
#save_dir = "大盤融資融券\\"
# 判斷程式是在何種作業系統執行以確認路徑撰寫方式
save_dir = ""
if sys.platform == "darwin" or sys.platform == "linux" :
    save_dir = "大盤融資融券/"
else :
    save_dir = "大盤融資融券\\"

current = start_date
while current <= end_date:
    date_str = current.strftime("%Y%m%d")
    file_name = f"大盤融資融券_{date_str}.txt"
    bk_file_name = f"BK_{file_name}"
    full_path = os.path.join(save_dir, file_name)

    print(f"處理檔案：{file_name}")

    if not os.path.exists(full_path):
        print("  !!! 檔案不存在，跳過")
        current += timedelta(days=1)
        continue

    try:
        # 備份原始檔案
        shutil.copy(full_path, os.path.join(save_dir, bk_file_name))

        # 讀取備份檔
        with open(os.path.join(save_dir, bk_file_name), 'r', encoding="utf-8", errors="ignore") as infile:
            data = infile.readlines()

        # 過濾資料
        filtered = []
        for line in data:
            if (re.search("項目", line) or
                re.search("交易單位", line) or
                re.search("仟元", line)):
                filtered.append(line)

        # 寫回原檔
        with open(full_path, 'w', encoding="utf-8") as outfile:
            outfile.writelines(filtered)

        print(f"  → {date_str} 格式化完成\n")

    except IOError as err:
        print(f"  !!! 檔案處理失敗：{err}\n")

    current += timedelta(days=1)

print("全部日期格式化處理完畢！")
"""
FormatTaiwanDataPolarisWithParams_V1.4.py
讀取檔案(CP950)格式化後另存為新檔(utf-8)
"""
import re
import sys
import shutil
import chardet

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        rawdata = f.read(20000)  # 讀取前 10KB
    result = chardet.detect(rawdata)
    return result['encoding']

if len(sys.argv) < 2:
    print("You need input one parameter(fmt : yyyymmdd)")
    sys.exit()

try:
    saveFileDir = "Files/" if sys.platform in ("darwin", "linux") else "Files\\"
    theFileName = sys.argv[1]
    input_file = theFileName + ".TXT"
    bk_input_file = "BK_" + input_file

    # 備份原始檔案
    shutil.copy(saveFileDir + input_file, saveFileDir + bk_input_file)

#   (20260523)若偵測為 Big5 或 CP950 → 統一用 CP950 讀
#    # 偵測編碼
#    encoding = detect_encoding(saveFileDir + bk_input_file)
#    print("檔案編碼偵測為:", encoding)
#    # 雖然偵測到的編碼可能是 CP950，但實際上可能是 Big5，因此這裡直接指定為 CP950 以確保正確讀取中文內容
#    # 確認資料：「00665L    富邦恒生國企正2 」，主要是"恒"字big5與cp950不同
#    encoding = "CP950"
    detected = detect_encoding(saveFileDir + bk_input_file)
    print("偵測到的編碼:", detected)
    
    if detected is None:
        encoding = "cp950"
    elif detected.lower() in ("big5", "cp950", "windows-1252"):
        encoding = "cp950"
    else:
        encoding = detected

    print("實際採用編碼:", encoding)

    # 讀取檔案內容（用偵測到的編碼）
    with open(saveFileDir + bk_input_file, 'r', encoding=encoding, errors="ignore") as infile:
        data = infile.readlines()

    # 寫回檔案，統一存成 UTF-8
    with open(saveFileDir + input_file, 'w', encoding="utf-8") as outfile:
        for line in data:
            if len(re.findall("^[0-9]{4}", line)) or len(re.findall("^[a-zA-Z][a-zA-Z0-9]", line)) > 0:
                outfile.write(line)
            else:
                print("omit rec:", line.strip())

    print("資料儲存完成!! 已轉換成 UTF-8")

except IOError as err:
    print("File error:", str(err))

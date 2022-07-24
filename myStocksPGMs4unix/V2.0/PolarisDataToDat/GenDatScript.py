import sys
import os 
import re

insertCnt = 0 
isFirstLine = True
try:
	if len(sys.argv) < 2 :
		print("You need input one parameter(fmt : YYYYMMDD)")
		print("syntax : C:\python GenDatScript.py 20170826")
		sys.exit()
	counts = 0
	find_YMD = sys.argv[1]
	DATA_DIR = "csv\\"
	outputFile = "__GenStocksDatScript.Bat"
	outfile = open(outputFile, 'w')
	
	file_data = []
	for filename in os.listdir(DATA_DIR):
		# 這應該是Python2的用法
#		print "Loading: %s" % filename
		print("Loading: {0}".format(filename))
		if filename.find(find_YMD) > 0 :
#			取得股票代號(改用正則表示式，因為檔名會有2個數字[股票代號、日期]，所以會回傳list)	
#			stockNo = filename[0:4]
			nums = re.findall(r"\d+", filename)
			print(nums)
			stockNo = nums[0]
			print(stockNo)
#           範例				
#			Python FormatFile.py 4126太醫日線-20171104.csv 4126.txt
#			Python InsertStocksFromPolarisToMySQLDB.py 4126 4126.txt
#			Python GetFileFromDB.py 4126
#			transFile2dat.exe 4126
			outfile.write("Python FormatFile.py " + filename + " " + stockNo + ".txt\n")
			outfile.write("Python InsertStocksFromPolarisToMySQLDB.py " + stockNo + " " + stockNo + ".txt\n")
			outfile.write("Python GetFileFromDB.py " + stockNo + "\n")
			outfile.write("transFile2dat.exe " + stockNo + "\n")
			outfile.write("\n")
			counts += 1

		# 下面這三行是做什用的??			
		loadFile = open(os.path.join(DATA_DIR, filename), 'rb')
		file_data.append(loadFile.read())
		loadFile.close()
	
	outfile.close()
	
except IOError as err :
	print('File error : ' + str(err))

print("資料處理完成!! 共 " + str(counts) + " 筆。")
